"""
ETL Pipeline для анализа продаж интернет-магазина
Этапы: Extract → Transform → Load → Visualize
"""

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sqlalchemy import create_engine, text
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SalesETLPipeline:
    """ETL пайплайн для обработки данных о продажах"""
    
    def __init__(self, csv_path, db_path='sales.db'):
        self.csv_path = csv_path
        self.db_path = db_path
        self.raw_data = None
        self.cleaned_data = None
        self.aggregated_data = None
        
    def extract(self):
        """
        Этап 1: Извлечение данных из CSV-файла
        TODO: Реализовать загрузку CSV с обработкой ошибок
        """
        logger.info("Начало этапа EXTRACT")
        
        # TODO: Загрузить CSV файл с помощью pandas
        # Обработать возможные ошибки (файл не найден, пустой файл)
        # Вывести информацию о количестве строк и колонок
        # Ваш код:
        try:
            self.raw_data = pd.read_csv(self.csv_path)
            logger.info(f"Загружено {len(self.raw_data)} строк, {len(self.raw_data.columns)} колонок")
        except FileNotFoundError:
            logger.error(f"Файл {self.csv_path} не найден")
            raise
        
        return self.raw_data
    
    def transform(self):
        """
        Этап 2: Трансформация и очистка данных
        TODO: Реализовать полную очистку данных
        """
        logger.info("Начало этапа TRANSFORM")
        
        df = self.raw_data.copy()
        print(df)
        print(len(df))
        print(df.isna().sum())
        # TODO 1: Удалить дубликаты (по всем колонкам)
        # Ваш код:
        
        #print(df.duplicated().tolist())
        df = df.drop_duplicates().reset_index(drop=True)
        

        # TODO 2: Обработать пропуски (NaN) в разных колонках
        # - Для числовых колонок: заменить на медиану
        # - Для текстовых: заменить на "Unknown"
        # Ваш код:

        n = ["quantity","price_per_unit"]
    
        df[n] = df[n].fillna(df[n].median())
        b = ["product_name","category","customer_name","customer_city","payment_method"]
        df[b] = df[b].fillna('Unknown')
        # TODO 3: Фильтрация аномалий (количество <= 0, цена <= 0)
        # Ваш код:
        df = df[
            (df['quantity'] > 0) &
            (df['price_per_unit'] > 0)
        ]
        
        # TODO 4: Преобразование типов данных
        # - order_date: в datetime
        # - quantity и price_per_unit: в числовые
        # Ваш код:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='raise')
        df['quantity'] = df['quantity'].astype(int)
        df['price_per_unit'] = df['price_per_unit'].astype(float)

        # TODO 5: Создать новую колонку total_amount = quantity * price_per_unit
        # Ваш код:
        df['total_amount'] = df['quantity'] * df['price_per_unit']

        # TODO 6: Обогащение данных (добавить колонку month_year из order_date)
        # Ваш код:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df.insert(2, "month_year", df['order_date'].dt.strftime('%B-%Y'))

        print(df)
        self.cleaned_data = df
        logger.info(f"После очистки: {len(df)} строк")
        
        return self.cleaned_data
    
    def aggregate(self):
        """
        Этап 3: Агрегация данных для аналитики
        TODO: Реализовать группировку по категориям
        """
        logger.info("Начало этапа AGGREGATE")
        
        df = self.cleaned_data.copy()
        
        # TODO: Сгруппировать по category и month_year, вычислить:
        # - total_quantity (сумма quantity)
        # - total_revenue (сумма total_amount)
        # - avg_price (средний price_per_unit)
        # - order_count (количество уникальных order_id)
        
        # Ваш код:
        self.aggregated_data = df.groupby(['category', 'month_year']).agg({
            'quantity': 'sum',
            'total_amount': 'sum',
            'price_per_unit': 'mean',
            'order_id': 'nunique'
        }).rename(columns={
            'quantity': 'total_quantity',
            'total_amount': 'total_revenue',
            'price_per_unit': 'avg_price',
            'order_id': 'order_count'
        }).reset_index()
        #print(self.aggregated_data)
        return self.aggregated_data
    
    def load_to_sqlite(self):
        """
        Этап 4: Загрузка данных в SQLite базу данных
        TODO: Сохранить очищенные и агрегированные данные в разные таблицы
        """
        logger.info("Начало этапа LOAD")
        
        # Создание подключения
        engine = create_engine(f'sqlite:///{self.db_path}')
        
        print(self.cleaned_data)
        # TODO 1: Сохранить cleaned_data в таблицу 'sales_cleaned'
        # Прямое SQL выражение
        with engine.connect() as conn:
        # Правильное создание таблицы
            conn.execute(text   ("""
                CREATE TABLE IF NOT EXISTS sales_cleaned (
                    order_id INTEGER PRIMARY KEY,
                    order_date DATE,
                    month_year TEXT,
                    product_name TEXT,
                    category TEXT,
                    quantity INTEGER,
                    price_per_unit REAL,
                    customer_name TEXT,
                    customer_city TEXT,
                    payment_method TEXT,
                    total_amount REAL
                )
            """))
            conn.commit()  # Для SQLite необязательно, но для других БД нужно
        self.cleaned_data.to_sql('sales_cleaned', engine, if_exists='replace', index=False)
        logger.info(f"Загружено {len(self.cleaned_data)} строк в таблицу sales_cleaned")


        # TODO 2: Сохранить aggregated_data в таблицу 'sales_aggregated'
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS sales_aggregated (
                    category TEXT,
                    month_year TEXT,
                    total_quantity INTEGER,
                    total_revenue REAL,
                    avg_price REAL,
                    order_count INTEGER
                )
            """))
            conn.commit() 
        self.aggregated_data.to_sql('sales_aggregated', engine, if_exists='replace', index=False)
        logger.info(f"Загружено {len(self.cleaned_data)} строк в таблицу sales_aggregated")
        # TODO 3: Если таблицы существуют - заменить (if_exists='replace')
        
        # Ваш код:
        
        logger.info(f"Данные загружены в {self.db_path}")
        
    def visualize(self):
        """Сохранение 3 графиков"""
        
        if self.aggregated_data is None:
            print("Нет данных для визуализации")
            return
        
        import os
        os.makedirs('plots', exist_ok=True)
        
        # Barplot
        self.aggregated_data.groupby('category')['total_revenue'].sum().plot(kind='bar')
        plt.title('Выручка по категориям')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('plots/barplot.png')
        plt.close()
        
        # Lineplot
        self.aggregated_data.groupby('month_year')['total_revenue'].sum().plot(kind='line', marker='o')
        plt.title('Динамика продаж')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('plots/lineplot.png')
        plt.close()
        
        # Pie chart
        self.aggregated_data.groupby('category')['total_revenue'].sum().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Доля категорий')
        plt.tight_layout()
        plt.savefig('plots/piechart.png')
        plt.close()
        
        print("✅ Графики сохранены в папку 'plots'")
    def run(self):
        """Запуск полного ETL-пайплайна"""
        logger.info("=" * 50)
        logger.info("ЗАПУСК ETL ПАЙПЛАЙНА")
        logger.info("=" * 50)
        
        self.extract()
        self.transform()
        self.aggregate()
        self.load_to_sqlite()
        self.visualize()
        
        logger.info("ETL пайплайн успешно завершён")


if __name__ == "__main__":
    # Создание и запуск пайплайна
    pipeline = SalesETLPipeline('data/sales.csv', 'sales.db')
    pipeline.run()