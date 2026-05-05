-- 1. Create Tables
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255),
    quantity INTEGER,
    price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES inventory(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50)
);

-- 2. Mock Data (Initial State)
INSERT INTO users (first_name, last_name, email) VALUES 
('John', 'Doe', 'john.doe@example.com'),
('Jane', 'Smith', 'jane.smith@example.com');

INSERT INTO inventory (product_name, quantity, price) VALUES 
('Laptop', 10, 999.99),
('Mouse', 50, 19.99),
('Keyboard', 30, 49.99);

INSERT INTO orders (user_id, product_id, status) VALUES 
(1, 1, 'PENDING'),
(2, 2, 'SHIPPED');


ALTER TABLE inventory REPLICA IDENTITY FULL;
ALTER TABLE users REPLICA IDENTITY FULL;
ALTER TABLE orders REPLICA IDENTITY FULL;
-- 3. Mock Updates (Test CDC)
-- Instructions: Run these one by one later to see them flow through Kafka/Flink
-- UPDATE inventory SET quantity = 9 WHERE product_name = 'Laptop';
-- UPDATE orders SET status = 'COMPLETED' WHERE id = 1;
-- DELETE FROM inventory WHERE product_name = 'Keyboard';
