-- Creating a view showing client_summary
CREATE VIEW olap.v_client_summary AS
SELECT
    c.client_id,
    c.full_name,
    c.country,
    c.state,
    c.city,
    COUNT(DISTINCT f.order_id) AS total_orders,
    SUM(f.total_amount) AS total_spent,
    ROUND(AVG(f.total_amount), 2) AS avg_order_value,
    MAX(d.date) AS last_order_date
FROM olap.dim_clients AS c
LEFT JOIN olap.fact_sales AS f
    ON c.client_id = f.client_id
LEFT JOIN olap.dim_date AS d
    ON f.date_id = d.date_id
GROUP BY c.client_id, c.full_name, c.state, c.city;





-- Creating a view for RFM
CREATE VIEW olap.v_rfm AS
SELECT
    client_id,
    full_name,
    CURRENT_DATE - last_order_date::DATE AS recency_days,
    total_orders AS frequency,
    total_spent AS monetary
FROM olap.v_client_summary;





-- Creating a view for RFM scoring
CREATE VIEW olap.v_rfm_scored AS
WITH scores AS(
    SELECT
        client_id,
        full_name,
        recency_days,
        frequency,
        monetary,
        NTILE(3) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(3) OVER (ORDER BY frequency) AS f_score,
        NTILE(3) OVER (ORDER BY monetary) AS m_score
    FROM olap.v_rfm
)
SELECT
    client_id,
    full_name,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) AS rfm_score,
    CASE
        WHEN (r_score + f_score + m_score) >= 8 THEN 'Gold'
        WHEN (r_score + f_score + m_score) >= 6 THEN 'Silver'
        ELSE 'Bronze'
    END AS segment
FROM scores
ORDER BY client_id;





-- Creating a view for analyzing churn risk
CREATE VIEW olap.v_churn_risk AS
WITH intervals AS (
    SELECT
        client_id,
        EXTRACT(EPOCH FROM (
            order_date - LAG(order_date) OVER (
                PARTITION BY client_id ORDER BY order_date
                )
            )) / 86400 AS days_between
    FROM oltp.orders
),
     avg_intervals AS (
         SELECT
             client_id,
             AVG(days_between) AS avg_days_between
         FROM intervals
         WHERE days_between IS NOT NULL
         GROUP BY client_id
     )
SELECT
    r.client_id,
    r.full_name,
    r.recency_days,
    ROUND(a.avg_days_between::NUMERIC, 1) AS avg_days_between,
    s.segment,
    CASE
        WHEN a.avg_days_between IS NULL THEN 'Unknown'
        WHEN r.recency_days > (a.avg_days_between * 4) THEN 'High'
        WHEN r.recency_days > (a.avg_days_between * 2) THEN 'Medium'
        ELSE 'Low'
        END AS churn_risk
FROM olap.v_rfm r
         JOIN olap.v_rfm_scored AS s
              ON r.client_id = s.client_id
         LEFT JOIN avg_intervals AS a
                   ON r.client_id = a.client_id;





-- Creating a view showing the most common category from which a given customer buys a product
CREATE VIEW olap.v_category_stats AS
WITH category_counts AS (
    SELECT
        s.client_id,
        c.full_name,
        p.category,
        COUNT(*) AS purchase_count,
        SUM(s.total_amount) AS category_spent,
        RANK() OVER (
            PARTITION BY s.client_id
            ORDER BY COUNT(*) DESC
            ) AS rnk
    FROM olap.fact_sales AS s
    JOIN olap.dim_products AS p
    ON s.product_id = p.product_id
    JOIN olap.dim_clients AS c
    ON s.client_id = c.client_id
    GROUP BY s.client_id, c.full_name, p.category
)
SELECT
    client_id,
    full_name,
    category AS most_bought_category,
    purchase_count,
    ROUND(category_spent::NUMERIC, 2) AS category_spent
FROM category_counts
WHERE rnk = 1;





-- Creating a view showing customer contact details
CREATE VIEW olap.v_client_contact AS
SELECT
    client_id,
    full_name,
    phone_number,
    email
FROM olap.dim_clients;