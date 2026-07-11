-- Creating view showing client_summary
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

/*
 Zrobić view dla RFM
 sprawdzić, czy dałoby się zrobić jakieś view z churn risk bez ML jak na razie
 zrobić view dla danych kontaktowych do klienta
 */