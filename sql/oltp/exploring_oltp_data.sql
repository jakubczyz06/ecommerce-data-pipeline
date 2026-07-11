-- Making SELECT queries for each table
SELECT *
FROM oltp.client_addresses;

SELECT *
FROM oltp.clients;

SELECT *
FROM oltp.order_items;

SELECT *
FROM oltp.orders
ORDER BY order_date DESC;

SELECT *
FROM oltp.products;