# **Лабораторная работа 15. Часть 1: Простой ETL-пайплайн на Python**

## **Тема:** ETL-процессы: извлечение, очистка, трансформация и загрузка данных с использованием Python.

### **Цель работы:**
Получить практические навыки построения ETL-пайплайна: загрузка данных из CSV, очистка и преобразование данных, агрегация, загрузка в базу данных SQLite и базовая визуализация результатов.

---

## **Задание: Построение ETL-пайплайна для анализа продаж интернет-магазина**

Вам предоставлен CSV-файл с данными о продажах. Необходимо построить ETL-пайплайн, который загружает данные, очищает их от пропусков и аномалий, агрегирует по категориям товаров и загружает результат в базу данных SQLite. Затем визуализировать полученные результаты.

### **1. Настройка проекта**

Установите необходимые Python-библиотеки в виртуальном окружении.

```bash
# Создание директории проекта
mkdir lab6_etl && cd lab6_etl

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Обновление pip
pip install --upgrade pip

# Установка библиотек
pip install pandas numpy sqlalchemy matplotlib seaborn jupyter
```

### **2. Базовый код (70% предоставляется)**

**Файл: `data/sales.csv` (исходные данные — создайте сами или используйте предоставленный)**

```csv
order_id,order_date,product_name,category,quantity,price_per_unit,customer_name,customer_city,payment_method
1001,2024-01-15,Ноутбук,Электроника,1,75000,Анна Смирнова,Москва,card
1002,2024-01-15,Мышь,Электроника,2,1500,Анна Смирнова,Москва,card
1003,2024-01-16,Книга SQL,Книги,1,2500,Петр Иванов,СПб,cash
1004,2024-01-16,,,1,1000,,,  # Строка с пропусками (проблемная)
1005,2024-01-17,Клавиатура,Электроника,-1,3000,Мария Сидорова,Казань,card  # Аномалия: отрицательное количество
1006,2024-01-17,Мышь,Электроника,3,1500,Мария Сидорова,Казань,card
1007,2024-01-18,Книга Python,Книги,1,3500,Иван Петров,Москва,card
1008,2024-01-18,Ноутбук,Электроника,1,85000,Елена Козлова,Новосибирск,cash
1009,2024-01-19,Монитор,Электроника,1,25000,Дмитрий Соколов,Екатеринбург,card
1010,2024-01-19,Книга SQL,Книги,2,2500,Ольга Новикова,Москва,cash
1010,2024-01-19,Книга SQL,Книги,2,2500,Ольга Новикова,Москва,cash  # Дубликат
```

**Файл: `etl_pipeline.py` (шаблон ETL-пайплайна)**

```python
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
from sqlalchemy import create_engine
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
        
        # TODO 1: Удалить дубликаты (по всем колонкам)
        # Ваш код:
        
        # TODO 2: Обработать пропуски (NaN) в разных колонках
        # - Для числовых колонок: заменить на медиану
        # - Для текстовых: заменить на "Unknown"
        # Ваш код:
        
        # TODO 3: Фильтрация аномалий (количество <= 0, цена <= 0)
        # Ваш код:
        
        # TODO 4: Преобразование типов данных
        # - order_date: в datetime
        # - quantity и price_per_unit: в числовые
        # Ваш код:
        
        # TODO 5: Создать новую колонку total_amount = quantity * price_per_unit
        # Ваш код:
        
        # TODO 6: Обогащение данных (добавить колонку month_year из order_date)
        # Ваш код:
        
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
        
        return self.aggregated_data
    
    def load_to_sqlite(self):
        """
        Этап 4: Загрузка данных в SQLite базу данных
        TODO: Сохранить очищенные и агрегированные данные в разные таблицы
        """
        logger.info("Начало этапа LOAD")
        
        # Создание подключения
        engine = create_engine(f'sqlite:///{self.db_path}')
        
        # TODO 1: Сохранить cleaned_data в таблицу 'sales_cleaned'
        # TODO 2: Сохранить aggregated_data в таблицу 'sales_aggregated'
        # TODO 3: Если таблицы существуют - заменить (if_exists='replace')
        
        # Ваш код:
        
        logger.info(f"Данные загружены в {self.db_path}")
        
    def visualize(self):
        """
        Этап 5: Визуализация результатов
        TODO: Создать 2-3 графика для анализа
        """
        logger.info("Начало этапа VISUALIZE")
        
        # TODO 1: График выручки по категориям (barplot)
        # Ваш код:
        
        # TODO 2: Динамика продаж по месяцам (lineplot)
        # Ваш код:
        
        # TODO 3: Доля категорий в общей выручке (pie chart)
        # Ваш код:
        
        plt.tight_layout()
        plt.show()
        
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
```

### **3. Задания для самостоятельного выполнения (30% дописать)**

#### **A. Реализация функции `extract()`** (обязательно)

Допишите метод `extract()` так, чтобы он:
- Загружал CSV с обработкой ошибок (файл не найден, пустой файл)
- Выводил информацию о структуре данных (типы колонок)
- Сохранял загруженные данные в `self.raw_data`

```python
# Ожидаемый результат после выполнения:
# 2024-01-20 10:00:00 - INFO - Загружено 12 строк, 7 колонок
# 2024-01-20 10:00:00 - INFO - Колонки: order_id, order_date, product_name, category, quantity, price_per_unit, customer_name, customer_city, payment_method
```

#### **B. Реализация полной очистки в `transform()`** (обязательно)

Выполните последовательно все шаги из TODO в методе `transform()`:

1. **Удаление дубликатов** — используйте `df.drop_duplicates()`
2. **Обработка пропусков**:
   - Для числовых колонок (`quantity`, `price_per_unit`): заполните медианным значением
   - Для текстовых колонок (`category`, `product_name`, `customer_name`): заполните "Unknown"
3. **Фильтрация аномалий**: удалите строки где `quantity <= 0` или `price_per_unit <= 0`
4. **Преобразование типов**:
   - `order_date = pd.to_datetime(df['order_date'], errors='coerce')`
   - `quantity` и `price_per_unit` приведите к `float` (ошибочные значения станут NaN, их потом удалите)
5. **Создание колонки `total_amount`**
6. **Создание колонки `month_year`** (формат: "2024-01")

```python
# Подсказка для month_year:
df['month_year'] = df['order_date'].dt.strftime('%Y-%m')
```

#### **C. Реализация загрузки в SQLite** (обязательно)

Допишите метод `load_to_sqlite()`:

```python
def load_to_sqlite(self):
    engine = create_engine(f'sqlite:///{self.db_path}')
    
    # Сохранение очищенных данных
    self.cleaned_data.to_sql('sales_cleaned', engine, if_exists='replace', index=False)
    
    # Сохранение агрегированных данных
    self.aggregated_data.to_sql('sales_aggregated', engine, if_exists='replace', index=False)
    
    # Проверка: вывести список таблиц в базе
    with engine.connect() as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        logger.info(f"Таблицы в БД: {tables}")
```

#### **D. Визуализация результатов** (дополнительно)

Создайте три графика:

1. **Выручка по категориям** (суммарно за весь период)
2. **Динамика продаж по месяцам** (линейный график с разбивкой по категориям)
3. **Круговая диаграмма** — доля каждой категории в общей выручке

```python
# Пример для графика 1:
def visualize(self):
    # Агрегация по категориям
    category_revenue = self.aggregated_data.groupby('category')['total_revenue'].sum().sort_values(ascending=False)
    
    plt.figure(figsize=(10, 6))
    category_revenue.plot(kind='bar', color='skyblue')
    plt.title('Выручка по категориям товаров', fontsize=14)
    plt.xlabel('Категория')
    plt.ylabel('Выручка (руб.)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

### **4. Запуск и проверка**

```bash
# Запуск ETL пайплайна
python etl_pipeline.py

# Проверка содержимого SQLite базы
sqlite3 sales.db
.tables
SELECT * FROM sales_aggregated;
.quit

# Альтернативная проверка через Python
python -c "import sqlite3; conn = sqlite3.connect('sales.db'); print(pd.read_sql('SELECT * FROM sales_aggregated', conn))"
```

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Полный код класса `SalesETLPipeline` с реализованными методами
   - Пример входного CSV (первые 5 строк)

2. **Скриншоты:**
   - Логи выполнения ETL-пайплайна (все этапы)
   - Результат запроса `SELECT * FROM sales_aggregated` (таблица в SQLite)
   - Три созданных графика

3. **Ответы на вопросы:**
   - Какие аномалии и пропуски были обнаружены в исходных данных? Как вы их обработали и почему?
   - В чём разница между ETL и ELT? Какой подход для данной задачи?
   - Почему в реальных проектах данные не загружают напрямую в базу без очистки?
   - Какие ещё трансформации могли бы быть полезны для этих данных?

### **6. Критерии оценивания:**

#### **Обязательные требования (минимум для зачёта):**
- **Extract:** Корректная загрузка CSV с обработкой ошибок (try-except)
- **Transform:** Удалены дубликаты, обработаны пропуски (числовые → медиана, текст → "Unknown"), удалены аномалии (quantity <= 0)
- **Load:** Данные успешно сохранены в SQLite (обе таблицы созданы)

#### **Дополнительные критерии (для повышения оценки):**
- **Визуализация:** Созданы 3 информативных графика с подписями осей и заголовками
- **Логирование:** Добавлено подробное логирование каждого этапа (количество удалённых дубликатов, пропусков)
- **Качество кода:** Использованы аннотации типов, docstring, обработка исключений

#### **Неприемлемые ошибки:**
- Пропуск обработки дубликатов (дубликат заказа 1010 остаётся)
- Игнорирование отрицательного количества товара (аномалия не удалена)
- Загрузка данных без преобразования типов (order_date остаётся строкой)

### **7. Полезные команды для Ubuntu:**

```bash
# Просмотр первых строк CSV
head -5 data/sales.csv

# Подсчёт строк в файле
wc -l data/sales.csv

# Запуск Python скрипта с профилированием
python -m cProfile etl_pipeline.py

# Просмотр размера базы данных
ls -lh sales.db

# Установка дополнительных библиотек
pip install pandas-profiling  # для расширенного анализа данных
```

### **8. Структура проекта:**

```
lab6_etl/
├── data/
│   └── sales.csv              # Исходные данные
├── etl_pipeline.py            # Основной ETL скрипт
├── sales.db                   # SQLite база (создаётся автоматически)
├── requirements.txt           # Зависимости проекта
├── logs/
│   └── etl.log               # Логи выполнения
└── report/
    ├── graphs/               # Сохранённые графики
    └── answers.md            # Ответы на вопросы
```

### **9. Советы по выполнению:**

1. **Тестируйте каждый этап отдельно:** Сначала добейтесь работы `extract()`, затем `transform()` и т.д.
2. **Используйте `.info()` и `.describe()`:** Они помогут увидеть пропуски и аномалии.
3. **Не удаляйте исходные данные:** Работайте с копией (`df.copy()`) на каждом этапе.
4. **Логируйте статистику:** Сколько строк удалено, сколько пропусков заполнено — это поможет в отчёте.
5. **Для визуализации используйте `seaborn`:** Он даёт более красивые графики с минимальным кодом.

```python
# Пример расширенной визуализации с seaborn
import seaborn as sns
sns.set_style("whitegrid")

plt.figure(figsize=(12, 6))
sns.barplot(data=category_revenue.reset_index(), x='category', y='total_revenue', palette='viridis')
plt.title('Выручка по категориям')
plt.xticks(rotation=45)
```

**Примечание:** В задании предоставлено ~70% кода (структура класса, заготовки методов, настройка логирования). Ваша задача — реализовать конкретные шаги трансформации и загрузки (помечены `TODO`).
