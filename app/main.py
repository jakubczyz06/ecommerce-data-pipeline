"""
Flask web application — e-commerce marketing analytics.

Routes:
  /                     → home page with client search + top clients
  /client/<client_id>   → full marketing profile of a single client
"""



# Imports
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import text

from app.db import engine
from utils.logger import get_logger



# Setting up the logger
logger = get_logger("app_flask")



# Flask application
app = Flask(__name__)



# Pagination — clients per page on list views
PER_PAGE = 50


def _get_page() -> int:
    """Reads ?page=N from the URL, defaults to 1, never below 1."""
    raw = request.args.get("page", "1")
    if not raw.isdigit():
        return 1
    return max(1, int(raw))





# Home page — search form + top clients + segment overview
@app.route("/")
def home():
    try:
        with engine.connect() as conn:
            top_clients = conn.execute(text("""
                SELECT
                    s.client_id,
                    s.full_name,
                    s.country,
                    s.state,
                    s.city,
                    s.total_orders,
                    s.total_spent,
                    ct.phone_number
                FROM olap.v_client_summary AS s
                JOIN olap.v_client_contact AS ct
                     ON s.client_id = ct.client_id
                WHERE s.total_spent IS NOT NULL
                ORDER BY s.total_spent DESC
                LIMIT 10
            """)).mappings().fetchall()

            segments = conn.execute(text("""
                SELECT segment, COUNT(*) AS client_count
                FROM olap.v_rfm_scored
                GROUP BY segment
                ORDER BY
                    CASE segment
                        WHEN 'Gold'   THEN 1
                        WHEN 'Silver' THEN 2
                        ELSE 3
                    END
            """)).mappings().fetchall()

            churn = conn.execute(text("""
                SELECT churn_risk, COUNT(*) AS client_count
                FROM olap.v_churn_risk
                GROUP BY churn_risk
            """)).mappings().fetchall()

        churn_map = {row["churn_risk"]: row["client_count"] for row in churn}

        return render_template(
            "index.html",
            top_clients = top_clients,
            segments    = segments,
            high_risk   = churn_map.get("High", 0),
        )

    except Exception as e:
        logger.error("Error on home page: %s", e)
        return "Server error — check logs", 500





# Search — accepts a client ID, a name fragment, or a phone number
@app.route("/search")
def search():
    query = request.args.get("client_id", "").strip()

    if not query:
        return redirect(url_for("home"))

    # Short numeric input → treat as client ID
    # (phone numbers have 10 digits, client IDs are much shorter)
    if query.isdigit() and len(query) <= 6:
        return redirect(url_for("client_profile", client_id = int(query)))

    # Text or phone-like input → search by full name OR phone number
    try:
        with engine.connect() as conn:
            matches = conn.execute(text("""
                SELECT
                    s.client_id,
                    s.full_name,
                    s.country,
                    s.state,
                    s.city,
                    s.total_orders,
                    s.total_spent,
                    ct.phone_number
                FROM olap.v_client_summary AS s
                JOIN olap.v_client_contact AS ct
                     ON s.client_id = ct.client_id
                WHERE s.full_name    ILIKE :q
                   OR ct.phone_number ILIKE :q
                ORDER BY s.full_name, s.client_id
                LIMIT 50
            """), {"q": f"%{query}%"}).mappings().fetchall()

        # Exactly one match → go straight to the profile
        if len(matches) == 1:
            return redirect(url_for(
                "client_profile",
                client_id = matches[0]["client_id"],
            ))

        # Zero or many → show the results page to choose from
        return render_template(
            "search_results.html",
            query   = query,
            matches = matches,
        )

    except Exception as e:
        logger.error("Error during search '%s': %s", query, e)
        return "Server error — check logs", 500





# Client profile — all analytical views for a single client
@app.route("/client/<int:client_id>")
def client_profile(client_id):
    try:
        with engine.connect() as conn:
            contact = conn.execute(text("""
                SELECT * FROM olap.v_client_contact
                WHERE client_id = :id
            """), {"id": client_id}).mappings().fetchone()

            if not contact:
                return render_template("client.html", not_found = True,
                                       client_id = client_id), 404

            summary = conn.execute(text("""
                SELECT * FROM olap.v_client_summary
                WHERE client_id = :id
            """), {"id": client_id}).mappings().fetchone()

            rfm = conn.execute(text("""
                SELECT * FROM olap.v_rfm_scored
                WHERE client_id = :id
            """), {"id": client_id}).mappings().fetchone()

            churn = conn.execute(text("""
                SELECT * FROM olap.v_churn_risk
                WHERE client_id = :id
            """), {"id": client_id}).mappings().fetchone()

            category = conn.execute(text("""
                SELECT * FROM olap.v_category_stats
                WHERE client_id = :id
            """), {"id": client_id}).mappings().fetchone()

        return render_template(
            "client.html",
            not_found = False,
            contact   = contact,
            summary   = summary,
            rfm       = rfm,
            churn     = churn,
            category  = category,
        )

    except Exception as e:
        logger.error("Error on client profile %s: %s", client_id, e)
        return "Server error — check logs", 500





# Segment list — all clients belonging to one RFM segment
@app.route("/segment/<segment_name>")
def segment_list(segment_name):
    segment = segment_name.capitalize()

    if segment not in ("Gold", "Silver", "Bronze"):
        return redirect(url_for("home"))

    page = _get_page()

    try:
        with engine.connect() as conn:
            total = conn.execute(text("""
                SELECT COUNT(*) FROM olap.v_rfm_scored
                WHERE segment = :seg
            """), {"seg": segment}).scalar()

            total_pages = max(1, -(-total // PER_PAGE))  # ceiling division
            page        = min(page, total_pages)

            clients = conn.execute(text("""
                SELECT
                    s.client_id,
                    s.full_name,
                    s.country,
                    s.state,
                    s.city,
                    s.total_orders,
                    s.total_spent,
                    ct.phone_number,
                    r.rfm_score AS extra_value
                FROM olap.v_rfm_scored AS r
                JOIN olap.v_client_summary AS s
                     ON r.client_id = s.client_id
                JOIN olap.v_client_contact AS ct
                     ON r.client_id = ct.client_id
                WHERE r.segment = :seg
                ORDER BY s.total_spent DESC NULLS LAST
                LIMIT :limit OFFSET :offset
            """), {
                "seg":    segment,
                "limit":  PER_PAGE,
                "offset": (page - 1) * PER_PAGE,
            }).mappings().fetchall()

        return render_template(
            "client_list.html",
            title       = f"{segment} clients",
            subtitle    = f"All clients in the {segment} RFM segment, "
                          f"sorted by total spend.",
            accent      = f"segment-{segment.lower()}",
            extra_label = "RFM score",
            clients     = clients,
            page        = page,
            total_pages = total_pages,
            total       = total,
        )

    except Exception as e:
        logger.error("Error on segment list '%s': %s", segment, e)
        return "Server error — check logs", 500





# Churn list — all clients flagged as high churn risk
@app.route("/churn-risk/high")
def churn_list():
    page = _get_page()

    try:
        with engine.connect() as conn:
            total = conn.execute(text("""
                SELECT COUNT(*) FROM olap.v_churn_risk
                WHERE churn_risk = 'High'
            """)).scalar()

            total_pages = max(1, -(-total // PER_PAGE))  # ceiling division
            page        = min(page, total_pages)

            clients = conn.execute(text("""
                SELECT
                    s.client_id,
                    s.full_name,
                    s.country,
                    s.state,
                    s.city,
                    s.total_orders,
                    s.total_spent,
                    ct.phone_number,
                    c.recency_days AS extra_value
                FROM olap.v_churn_risk AS c
                JOIN olap.v_client_summary AS s
                     ON c.client_id = s.client_id
                JOIN olap.v_client_contact AS ct
                     ON c.client_id = ct.client_id
                WHERE c.churn_risk = 'High'
                ORDER BY s.total_spent DESC NULLS LAST
                LIMIT :limit OFFSET :offset
            """), {
                "limit":  PER_PAGE,
                "offset": (page - 1) * PER_PAGE,
            }).mappings().fetchall()

        return render_template(
            "client_list.html",
            title       = "High churn risk",
            subtitle    = "Clients who have not purchased for much longer "
                          "than their usual buying rhythm.",
            accent      = "risk-high",
            extra_label = "Days since last order",
            clients     = clients,
            page        = page,
            total_pages = total_pages,
            total       = total,
        )

    except Exception as e:
        logger.error("Error on churn list: %s", e)
        return "Server error — check logs", 500





if __name__ == "__main__":
    app.run(debug = True)
