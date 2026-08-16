# E-commerce-Analytics-Web-App

A full-stack web application and data engineering pipeline built for the made-up American electronics e-commerce retailer. This project provides a comprehensive dashboard for customer identification, behavioral analysis, and proactive retention using RFM segmentation and Churn Risk scoring.

This repository showcases an end-to-end data lifecycle: from generating synthetic datasets and building an ETL pipeline, to designing a Star Schema data warehouse (OLAP) and serving insights through a Flask web interface.

---

## Key Features

* **Custom Synthetic Data Generation:** Python script using `Faker` and `pandas` that generates a realistic, seeded dataset of 5,000 clients, 260 electronic SKUs, and 50,000 orders.
* **End-to-End ETL Pipeline:** Automated extraction of CSV data, loading into a staging area (Raw), and transforming it into a fully normalized transactional database (OLTP).
* **Data Warehouse (Star Schema):** An analytical OLAP layer utilizing dimension and fact tables to optimize complex aggregations and reporting.
* **Advanced Customer Analytics:**
* **RFM Segmentation:** Automatically classifies customers into *Gold*, *Silver*, and *Bronze* tiers based on Recency, Frequency, and Monetary value.
* **Churn Risk Scoring:** Calculates the probability of a customer leaving based on dynamic, per-segment thresholds.


* **Interactive Flask Dashboard:** A user-friendly web interface featuring customer search, paginated lists of customer segments, and detailed individual profiles with purchase preferences and contact capabilities.

---

## Architecture Flow

The data flows from raw generation through a structured database architecture before being served to the frontend.

```text
[ Synthetic Data Generator ] 
            │
            ▼
       ( CSV Files )
            │
            ▼
    [ Raw Schema (Staging) ]
            │
      ( ETL Pipeline )
            │
            ▼
[ OLTP Schema (Normalized DB) ]
            │
       ( Transform )
            │
            ▼
 [ OLAP Schema (Star Schema) ] ────┐
            │                      │
       ( SQL Views )               │
            │                      │
            ▼                      ▼
  [ Flask Backend ] ───────► [ HTML/CSS Dashboard ]

```

---

## Tech Stack

* **Data Engineering & Backend:** Python 3, `pandas`, `Faker`, SQLAlchemy, Flask
* **Database:** PostgreSQL (OLTP & OLAP design, Views, Star Schema)
* **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## How to Run Locally

Follow these steps to set up the project on your local machine.

**1. Clone the repository and navigate to the directory:**

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

```

**2. Set up a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

```

**3. Configure Environment Variables:**
Create a `.env` file in the root directory and add your PostgreSQL credentials:

```ini
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db

```

**4. Initialize the Database:**
Execute the SQL scripts in the correct order to create schemas, tables, and views.
*(Note: You can run these via pgAdmin, DBeaver, or psql)*

**5. Generate Data and Run the Pipeline:**

```bash
python scripts/generator.py  # Generates the synthetic CSV data
python scripts/etl.py        # Runs the ETL pipeline (CSV -> Raw -> OLTP -> OLAP)

```

**6. Launch the Web Application:**

```bash
flask run

```

The dashboard will be available at `http://localhost:5000`.

---

## Roadmap & Future Improvements

**v2.0 (Next Iteration)**

* [ ] **ELT Refactor:** Transition to an Extract-Load-Transform paradigm treating OLTP as the primary source.
* [ ] **Database Optimization:** Implement B-Tree/Bitmap indexes and Materialized Views for faster dashboard load times.

**Backlog**

* [ ] **Containerization:** Wrap the application and database in Docker & Docker Compose for seamless deployment.
