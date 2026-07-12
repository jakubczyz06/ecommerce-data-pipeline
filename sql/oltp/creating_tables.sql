-- Creating schema for public tables
CREATE SCHEMA IF NOT EXISTS oltp;





-- Ensuring that there are no duplicates
DROP TABLE IF EXISTS oltp.clients CASCADE;
DROP TABLE IF EXISTS oltp.client_addresses CASCADE;
DROP TABLE IF EXISTS oltp.orders CASCADE;
DROP TABLE IF EXISTS oltp.order_items CASCADE;
DROP TABLE IF EXISTS oltp.products CASCADE;





-- Creating public tables
CREATE TABLE oltp.clients (
    client_id INT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender CHAR(1),
    phone_number VARCHAR(20),
    email VARCHAR(254) NOT NULL,
    registration_date TIMESTAMP NOT NULL
);


CREATE TABLE oltp.client_addresses (
    address_id INT PRIMARY KEY ,
    client_id INT REFERENCES oltp.clients(client_id) ON DELETE CASCADE,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    postal_code VARCHAR(20),
    street VARCHAR(100),
    building_number VARCHAR(50),
    apartament_number VARCHAR(50),
    address_type VARCHAR(50)
);


CREATE TABLE oltp.orders (
    order_id INT PRIMARY KEY,
    client_id INT REFERENCES oltp.clients(client_id) ON DELETE CASCADE,
    order_date TIMESTAMP NOT NULL,
    order_status VARCHAR(50) NOT NULL
);


CREATE TABLE oltp.products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    screen_size VARCHAR(20),
    unit_price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL
);


CREATE TABLE oltp.order_items (
    order_item_id INT PRIMARY KEY,
    order_id INT REFERENCES oltp.orders(order_id) ON DELETE CASCADE,
    product_id INT REFERENCES oltp.products(product_id) ON DELETE CASCADE,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL
);