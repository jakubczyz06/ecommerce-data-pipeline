-- Inserting data into date dimension
INSERT INTO olap.dim_date
SELECT
    TO_CHAR(d, 'YYYYMMDD')::INT AS date_id,
    d::TIMESTAMP AS date,
    EXTRACT(YEAR FROM d)::INT AS year,
    EXTRACT(QUARTER FROM d)::INT AS quarter,
    EXTRACT(MONTH FROM d)::INT AS month,
    TO_CHAR(d, 'FMMonth') AS month_name,
    EXTRACT(WEEK FROM d)::INT AS week,
    EXTRACT(DAY FROM d)::INT AS day,
    TO_CHAR(d, 'FMDay') AS day_name,
    CASE
        WHEN EXTRACT(DOW FROM d) IN (0,6) THEN 0
        ELSE 1
    END
FROM GENERATE_SERIES(
    '2022-01-01'::DATE,
    '2027-12-31'::DATE,
    '1 day'::INTERVAL
) AS d;





-- Inserting data into clients dimension
INSERT INTO olap.dim_clients
SELECT
    c.client_id,
    c.full_name,
    c.gender,
    c.phone_number,
    c.email,
    c.registration_date,
    ca.country,
    ca.state,
    ca.city
FROM oltp.clients AS c
LEFT JOIN oltp.client_addresses AS ca
    ON c.client_id = ca.client_id
    AND ca.address_type IN ('billing_and_shipping', 'billing');





-- Inserting data into products dimension
INSERT INTO olap.dim_products
SELECT
    product_id,
    product_name,
    category,
    brand,
    screen_size
FROM oltp.products;





-- Inserting data into fact_sales table
INSERT INTO olap.fact_sales
SELECT
    o.client_id,
    oi.product_id,
    d.date_id,
    o.order_id,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS total_amount
FROM oltp.orders AS o
         JOIN oltp.order_items AS oi
              ON o.order_id = oi.order_id
         JOIN olap.dim_date AS d
              ON TO_CHAR(o.order_date, 'YYYYMMDD')::INT = d.date_id;