-- Creating schema for raw tables
CREATE SCHEMA IF NOT EXISTS raw;





-- Ensuring that there are no duplicates
DROP TABLE IF EXISTS raw.clients CASCADE;
DROP TABLE IF EXISTS raw.client_addresses CASCADE;
DROP TABLE IF EXISTS raw.orders CASCADE;
DROP TABLE IF EXISTS raw.order_items CASCADE;
DROP TABLE IF EXISTS raw.products CASCADE;





-- Creating raw tables
CREATE TABLE raw.clients (
    client_id TEXT,
    full_name TEXT,
    gender TEXT,
    phone_number TEXT,
    email TEXT,
    registration_date TEXT
    );


CREATE TABLE raw.client_addresses (
    address_id TEXT,
    client_id TEXT,
    country TEXT,
    state TEXT,
    city TEXT,
    postal_code TEXT,
    street TEXT,
    building_number TEXT,
    apartament_number TEXT,
    address_type TEXT
);


CREATE TABLE raw.orders (
    order_id TEXT,
    client_id TEXT,
    order_date TEXT,
    order_status TEXT
);


CREATE TABLE raw.products (
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    screen_size TEXT,
    unit_price TEXT,
    created_at TEXT
);


CREATE TABLE raw.order_items (
    order_item_id TEXT,
    order_id TEXT,
    product_id TEXT,
    quantity TEXT,
    unit_price TEXT
);