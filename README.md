# E-commerce-Analytics-Web-App

A full-stack web application and data engineering pipeline built for a made-up American electronics e-commerce retailer. This project provides a comprehensive dashboard for customer identification, behavioral analysis, and proactive retention using RFM segmentation and Churn Risk scoring.

This repository showcases an end-to-end data lifecycle: from generating synthetic datasets and building an ETL pipeline, to designing a Star Schema data warehouse (OLAP) and serving insights through a Flask web interface.

![Main page](docs/image1.png)
*The view of the main page*

---

## Key Features

* **Custom Synthetic Data Generation:** Python script using `Faker` and `pandas` that generates a realistic, seeded dataset up to 5,000 clients, 260 electronic SKUs, and 50,000 orders.
  
* **End-to-End ETL Pipeline:** Automated extraction of CSV data, loading into a staging area (Raw), and transforming it into a fully normalized transactional database (OLTP).
  
* **Data Warehouse (Star Schema):** An analytical OLAP layer utilizing dimension and fact tables to optimize complex aggregations and reporting.
  
* **Advanced Customer Analytics:**
  * **RFM Segmentation:** classifies customers into *Gold*, *Silver*, and *Bronze* tiers based on Recency, Frequency, and Monetary value.
  * **Churn Risk Scoring:** calculates the probability of a customer leaving based on dynamic, per-segment thresholds.
    
* **Customer Details:** Shows all known details of each customer (their address, purchase summary, contact info, and favorite category).
 
* **Interactive Flask Dashboard:** A user-friendly web interface featuring customer search, paginated lists of customer segments, and detailed individual profiles with purchase preferences and contact capabilities.

![Customer analysis page](docs/image2.png)
*The view of the customer analysis page*

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

* **Data Engineering & Backend:** Python 3, pandas, numpy, Faker, SQLAlchemy, Flask, dotenv
  
* **Database:** PostgreSQL (OLTP & OLAP design, Views, Star Schema)
  
* **Frontend:** HTML5, CSS3, Jinja2 Templates

---

## Project Structure

```text
├── data_generator/       # Synthetic data generation (Faker + pandas)
│   ├── config.py
│   ├── main.py
│   └── generators/
├── etl/                  # ETL pipeline: CSV → raw → OLTP
│   ├── extract/
│   ├── transform/
│   ├── load/
│   └── main.py
├── sql/                  # Database schema and warehouse SQL
│   ├── raw/
│   ├── oltp/
│   └── olap/
├── app/                  # Flask web application
│   ├── main.py
│   ├── db.py
│   ├── templates/
│   └── static/
├── utils/                # Shared logger and path helpers
│   ├── logger.py
│   └── paths.py
└── requirements.txt
```

---

## How to Run Locally

Follow these steps to set up the project on your local machine.

**1. Clone the repository and navigate to the directory:**

```bash
git clone https://github.com/jakubczyz06/E-commerce-Analytics-Web-App.git
cd E-commerce-Analytics-Web-App
```

**2. Set up a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure Environment Variables:**

Create a `.env` file in the project root (see `.env.example` in docs/) and add your PostgreSQL connection string:

```ini
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/ecommerce_db
```

**4. Initialize the Database:**

Create a PostgreSQL database named `ecommerce_db`, then run the SQL scripts in this exact order (via psql, pgAdmin, or DataGrip):

```bash
psql -d ecommerce_db -f sql/raw/creating_tables.sql
psql -d ecommerce_db -f sql/oltp/creating_tables.sql
psql -d ecommerce_db -f sql/olap/creating_tables.sql
```

**5. Generate Data and Run the ETL Pipeline:**

*(Note: pass `--mode SMALL`, `MEDIUM`, or `LARGE` to control the dataset size)*

```bash
python data_generator/main.py --mode SMALL   # Generates the synthetic CSV data
python etl/main.py                           # Runs the ETL pipeline (CSV -> raw -> OLTP)
```

**6. Build the Data Warehouse:**

```bash
psql -d ecommerce_db -f sql/olap/inserting_data.sql
psql -d ecommerce_db -f sql/olap/creating_views.sql
```

**7. Launch the Web Application:**

```bash
python -m app.main
```

The dashboard will be available at `http://localhost:5000`.

---

## Roadmap & Future Improvements

**v2.0 (Next Iteration)**

* [ ] **ELT Refactor:** Transition to an Extract-Load-Transform paradigm treating OLTP as the primary source.
* [ ] **Database Optimization:** Implement B-Tree indexes and Materialized Views for faster dashboard load times.
* [ ] **Containerization:** Wrap the application and database in Docker & Docker Compose for seamless deployment.

**v3.0**

* [ ] **Workflow Orchestration:** Introduce Apache Airflow to schedule and monitor data pipeline runs.
* [ ] **Machine Learning:** Implement an algorithm to predict customer churn risk.
