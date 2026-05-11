-- Создание индекса
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);

-- Анализ плана выполнения ДО создания индекса
EXPLAIN ANALYZE SELECT * FROM order_items WHERE order_id = 1;

-- После создания индекса выполните ещё раз
-- EXPLAIN ANALYZE SELECT * FROM order_items WHERE order_id = 1;
