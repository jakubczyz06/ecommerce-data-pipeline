-- Creating schema for analytical tables
CREATE SCHEMA IF NOT EXISTS olap;





-- Ensuring that there are no duplicates
DROP TABLE IF EXISTS olap.dim_date CASCADE;
DROP TABLE IF EXISTS olap.dim_clients CASCADE;
DROP TABLE IF EXISTS olap.dim_products CASCADE;
DROP TABLE IF EXISTS olap.fact_sales CASCADE;





-- Creating analytical tables basing on star schema
CREATE TABLE olap.dim_date (
    date_id INT PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    week INT,
    day INT,
    day_name VARCHAR(20),
    if_workday INT
);


CREATE TABLE olap.dim_clients (
    client_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender CHAR(1),
    phone_number VARCHAR(20),
    email VARCHAR(254) NOT NULL,
    registration_date TIMESTAMP NOT NULL,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100)
);


CREATE TABLE olap.dim_products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    screen_size VARCHAR(20)
);


CREATE TABLE olap.fact_sales (
    client_id INT REFERENCES olap.dim_clients(client_id),
    product_id INT REFERENCES olap.dim_products(product_id),
    date_id INT REFERENCES olap.dim_date(date_id),
    order_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price   NUMERIC(10,2),
    total_amount NUMERIC(10,2)
);
