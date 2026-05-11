-- Создание таблиц
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    stock_quantity INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL
);

-- Вставка тестовых данных
INSERT INTO users (email, full_name) VALUES
    ('alice@example.com', 'Alice Smith'),
    ('bob@example.com', 'Bob Johnson');

INSERT INTO products (name, category, price, stock_quantity) VALUES
    ('Ноутбук', 'Электроника', 75000.00, 10),
    ('Мышь', 'Электроника', 1500.00, 50),
    ('Книга SQL', 'Книги', 2500.00, 30),
    ('Web camera', 'Электроника', 1500.00, 10),
    ('USB флешка', 'Электроника', 500.00, 50),
    ('Кружка', 'Посуда', 400.00, 30);

-- Вставка заказов
INSERT INTO orders (user_id, status) VALUES
    (1, 'pending'),   -- заказ Alice
    (2, 'completed'),   -- заказ Bob
    (3, 'completed');   -- заказ Alice

-- Вставка позиций заказов
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 6, 1, 400.00),  -- Кружка в заказе Alice
    (1, 4, 1, 1500.00),   -- Web camera в заказе Alice
    (2, 3, 1, 2500.00),   -- Книга SQL в заказе Bob
    (3, 2, 1, 1500.00),   -- Мышь в заказе Alice
    (4, 1, 4, 75000.00);  -- Кружка в заказе Alice

