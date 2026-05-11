import sqlite3
import pandas as pd

# Подключение к базе
conn = sqlite3.connect('sales.db')  # или ваш путь

# Просмотр всех таблиц
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Таблицы в базе:")
print(tables)

# Просмотр данных из sales_cleaned
df = pd.read_sql("SELECT * FROM sales_cleaned", conn)
print("\nСодержимое sales_cleaned:")
print(df)

df = pd.read_sql("SELECT * FROM sales_aggregated", conn)
print("\nСодержимое sales_aggregated:")
print(df)

# Закрываем соединение
conn.close()