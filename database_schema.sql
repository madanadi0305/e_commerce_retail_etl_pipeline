-- E-Commerce Analytics Database Schema
-- PostgreSQL Database: e_commerce_analytics

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS sales_summary CASCADE;

-- Create Orders Table
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    order_added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    order_updated_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    shipping_address TEXT,
    CONSTRAINT chk_quantity CHECK (quantity > 0),
    CONSTRAINT chk_price CHECK (price >= 0),
    CONSTRAINT chk_total CHECK (total_amount >= 0)
);

-- Create Products Table
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 0,
    product_added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    product_updated_at TIMESTAMP,
    description TEXT,
    brand VARCHAR(100),
    CONSTRAINT chk_product_price CHECK (price >= 0),
    CONSTRAINT chk_product_quantity CHECK (quantity >= 0)
);

-- Create Customers Table
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    total_orders INTEGER DEFAULT 0,
    customer_added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    customer_updated_at TIMESTAMP,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(20),
    phone_number VARCHAR(20),
    CONSTRAINT chk_total_orders CHECK (total_orders >= 0)
);

-- Create Sales Summary Table
CREATE TABLE sales_summary (
    id SERIAL PRIMARY KEY,
    total_revenue DECIMAL(15, 2) NOT NULL,
    total_orders INTEGER NOT NULL,
    total_customers INTEGER NOT NULL,
    sales_summary_added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_revenue CHECK (total_revenue >= 0),
    CONSTRAINT chk_orders CHECK (total_orders >= 0),
    CONSTRAINT chk_customers CHECK (total_customers >= 0)
);

-- Create Indexes for better query performance
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_product_id ON orders(product_id);
CREATE INDEX idx_orders_added_at ON orders(order_added_at);
CREATE INDEX idx_orders_status ON orders(status);

CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_added_at ON products(product_added_at);
CREATE INDEX idx_products_brand ON products(brand);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_added_at ON customers(customer_added_at);
CREATE INDEX idx_customers_country ON customers(country);

CREATE INDEX idx_sales_summary_added_at ON sales_summary(sales_summary_added_at);

-- Create Views for Analytics

-- View: Recent Orders (Last 30 days)
CREATE OR REPLACE VIEW recent_orders AS
SELECT 
    o.order_id,
    o.customer_id,
    c.customer_name,
    o.product_id,
    o.product_name,
    o.quantity,
    o.price,
    o.total_amount,
    o.status,
    o.order_added_at
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_added_at >= CURRENT_TIMESTAMP - INTERVAL '30 days'
ORDER BY o.order_added_at DESC;

-- View: Product Sales Summary
CREATE OR REPLACE VIEW product_sales_summary AS
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.brand,
    COUNT(o.order_id) as total_orders,
    SUM(o.quantity) as total_units_sold,
    SUM(o.total_amount) as total_revenue,
    AVG(o.price) as average_price
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
GROUP BY p.product_id, p.product_name, p.category, p.brand;

-- View: Customer Purchase Summary
CREATE OR REPLACE VIEW customer_purchase_summary AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.city,
    c.state,
    c.country,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as average_order_value,
    MAX(o.order_added_at) as last_order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name, c.email, c.city, c.state, c.country;

-- View: Daily Sales Report
CREATE OR REPLACE VIEW daily_sales_report AS
SELECT 
    DATE(order_added_at) as sale_date,
    COUNT(order_id) as total_orders,
    SUM(quantity) as total_items_sold,
    SUM(total_amount) as total_revenue,
    AVG(total_amount) as average_order_value
FROM orders
GROUP BY DATE(order_added_at)
ORDER BY sale_date DESC;

-- Insert Sample Data (Optional)
INSERT INTO customers (customer_id, customer_name, email, total_orders, city, state, country, zip_code, phone_number) VALUES
('CUST001', 'John Doe', 'john@example.com', 5, 'New York', 'NY', 'USA', '10001', '243-345-6789'),
('CUST002', 'Jane Smith', 'jane@example.com', 3, 'Seattle', 'WA', 'USA', '98101', '243-345-6789');

INSERT INTO products (product_id, product_name, category, price, quantity, description, brand) VALUES
('PROD001', 'Wireless Headphones', 'Electronics', 70.00, 150, 'High-quality wireless headphones with noise cancellation', 'TechAudio'),
('PROD002', 'Smart Watch', 'Electronics', 200.00, 75, 'Feature-rich smartwatch with fitness tracking', 'FitTech'),
('PROD003', 'Laptop Stand', 'Accessories', 30.00, 200, 'Ergonomic aluminum laptop stand', 'DeskPro');

INSERT INTO orders (order_id, customer_id, product_id, product_name, quantity, price, total_amount, status, payment_method, shipping_address) VALUES
('ORD001', 'CUST001', 'PROD001', 'Wireless Headphones', 2, 70.00, 140.00, 'completed', 'credit_card', '123 Main St, New York, NY 10001'),
('ORD002', 'CUST002', 'PROD002', 'Smart Watch', 1, 200.00, 200.00, 'pending', 'paypal', '456 Oak Ave, Seattle, WA 98101');

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_user;
