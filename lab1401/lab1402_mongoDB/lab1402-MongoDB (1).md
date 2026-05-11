# **Лабораторная работа 14. Часть 2: NoSQL базы данных на примере MongoDB**

## **Тема:** Документные базы данных: CRUD-операции, агрегационные пайплайны и сравнение с реляционной моделью.

### **Цель работы:**
Получить практические навыки работы с документной NoSQL СУБД MongoDB: выполнение CRUD-операций, построение агрегационных пайплайнов и сравнение подходов к организации данных с реляционной моделью.

---

## **Задание: Разработка запросов для интернет-магазина в MongoDB**

Вам необходимо создать базу данных для того же интернет-магазина (как в Части 1), но в документной модели MongoDB. Затем выполнить CRUD-операции и агрегационные запросы, сравнить подходы.

### **1. Настройка проекта**

Используйте облачную версию MongoDB Atlas (бесплатный тариф) или локальную установку.

#### **Вариант A: MongoDB Atlas (рекомендуется)**

```bash
# 1. Зарегистрируйтесь на https://www.mongodb.com/cloud/atlas
# 2. Создайте бесплатный кластер (M0)
# 3. Создайте пользователя и запишите пароль
# 4. Добавьте IP-адрес 0.0.0.0/0 (для доступа из любого места)
# 5. Получите строку подключения вида:
#    mongodb+srv://username:password@cluster.mongodb.net/
```

#### **Вариант B: Локальная установка на Ubuntu**

```bash
# Импорт публичного ключа MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -

# Добавление репозитория
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

# Установка MongoDB
sudo apt update
sudo apt install mongodb-org

# Запуск службы
sudo systemctl start mongod
sudo systemctl enable mongod

# Подключение к MongoDB
mongosh
```

#### **Установка MongoDB Compass (графический интерфейс)**

```bash
# Скачайте .deb файл с официального сайта
# Или используйте встроенный интерфейс MongoDB Atlas
```

### **2. Базовый код (70% предоставляется)**

**База данных: `shop_mongo`**
**Коллекции: `users`, `products`, `orders`**

```javascript
// Переключение на базу данных
use shop_mongo;

// ========== 1. СОЗДАНИЕ КОЛЛЕКЦИЙ И ДОКУМЕНТОВ ==========

// Коллекция users (документы с вложенной структурой)
db.users.insertMany([
    {
        _id: 1,
        email: "alice@example.com",
        full_name: "Alice Smith",
        created_at: new Date(),
        address: {
            city: "Moscow",
            street: "Tverskaya",
            zipcode: "101000"
        }
    },
    {
        _id: 2,
        email: "bob@example.com", 
        full_name: "Bob Johnson",
        created_at: new Date(),
        address: {
            city: "Saint Petersburg",
            street: "Nevsky",
            zipcode: "191186"
        }
    }
]);

// Коллекция products
db.products.insertMany([
    {
        _id: 1,
        name: "Ноутбук",
        category: "Электроника",
        price: 75000,
        stock_quantity: 10,
        specs: {
            brand: "Lenovo",
            ram: "16GB",
            storage: "512GB SSD"
        }
    },
    {
        _id: 2,
        name: "Мышь",
        category: "Электроника",
        price: 1500,
        stock_quantity: 50
    },
    {
        _id: 3,
        name: "Книга SQL",
        category: "Книги",
        price: 2500,
        stock_quantity: 30,
        specs: {
            author: "Дмитрий К.",
            pages: 450
        }
    }
]);

// TODO: Добавьте ещё 2 продукта самостоятельно (см. задание A)
// TODO: Создайте заказы (каждый заказ содержит массив товаров)
```

### **3. Задания для самостоятельного выполнения (30% дописать)**

#### **A. Добавление тестовых данных** (обязательно)

Добавьте **минимум 2 заказа** в документном формате. В отличие от SQL, заказы должны содержать вложенный массив `items`.

```javascript
// TODO: Вставьте 2 заказа (один для Alice, один для Bob)
// Каждый заказ должен содержать:
// - user_id (ссылка на пользователя)
// - order_date
// - status (pending/completed/cancelled)
// - items: массив объектов с product_id, quantity, price_at_moment

db.orders.insertMany([
    {
        _id: 1,
        user_id: 1,  // Alice
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 1, quantity: 1, price: 75000 },  // Ноутбук
            { product_id: 2, quantity: 2, price: 1500 }    // Мышь x2
        ]
    },
    {
        _id: 2,
        user_id: 2,  // Bob
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 3, quantity: 1, price: 2500 }     // Книга SQL
        ]
    }
    // TODO: добавьте третий заказ (любой)
]);
```

#### **B. CRUD-операции** (обязательно)

Реализуйте следующие операции:

**1. READ: Найти все заказы пользователя Alice с суммой заказа**

```javascript
// TODO: Используйте lookup и агрегацию
db.orders.aggregate([
    {
        $lookup: {
            from: "users",
            localField: "user_id",
            foreignField: "_id",
            as: "user_info"
        }
    },
    { $unwind: "$user_info" },
    { $match: { "user_info.email": "alice@example.com" } },
    {
        $addFields: {
            total_amount: {
                $sum: { $map: {
                    input: "$items",
                    as: "item",
                    in: { $multiply: ["$$item.quantity", "$$item.price"] }
                }}
            }
        }
    }
]);
```

**2. UPDATE: Добавить поле `discount` к заказам дороже 80000 руб.**

```javascript
// TODO: Обновите заказы, у которых total_amount > 80000
// Подсказка: сначала вычислите сумму, затем обновите

// Ваш код:
db.orders.updateMany(
    { /* условие */ },
    { $set: { discount: 10 } }  // 10% скидка
);
```

**3. DELETE: Удалить заказы со статусом "cancelled" старше 30 дней**

```javascript
// TODO: Вычислите дату 30 дней назад и удалите отменённые заказы
// Ваш код:
const thirtyDaysAgo = new Date();
thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

db.orders.deleteMany({
    status: "cancelled",
    order_date: { $lt: thirtyDaysAgo }
});
```

#### **C. Агрегационный пайплайн** (обязательно)

Постройте отчёт по категориям товаров (аналогично Части 1, задание 2):

```javascript
// TODO: Выведите для каждой категории:
// - общее количество проданных единиц
// - общую выручку
// - среднюю цену продажи
// Отсортируйте по убыванию выручки

db.orders.aggregate([
    // Шаг 1: Развернуть массив items
    { $unwind: "$items" },
    
    // Шаг 2: Соединить с products (получить категорию)
    {
        $lookup: {
            from: "products",
            localField: "items.product_id",
            foreignField: "_id",
            as: "product_info"
        }
    },
    { $unwind: "$product_info" },
    
    // TODO: Шаг 3 - Группировка по категории с суммированием
    
    // TODO: Шаг 4 - Сортировка по выручке
    
    // TODO: Шаг 5 - Проекция (переименование полей)
]);
```

#### **D. Сравнение моделей данных** (дополнительно)

Реализуйте те же запросы, что в Части 1 (PostgreSQL), но в MongoDB:

1. **Топ-3 пользователя по сумме заказов**
2. **Заказы с итоговой суммой (аналог JOIN users)**

```javascript
// Пример: топ-3 пользователей
db.orders.aggregate([
    { $unwind: "$items" },
    {
        $group: {
            _id: "$user_id",
            total_spent: {
                $sum: { $multiply: ["$items.quantity", "$items.price"] }
            }
        }
    },
    { $sort: { total_spent: -1 } },
    { $limit: 3 },
    {
        $lookup: {
            from: "users",
            localField: "_id",
            foreignField: "_id",
            as: "user"
        }
    },
    { $unwind: "$user" },
    {
        $project: {
            full_name: "$user.full_name",
            total_spent: 1
        }
    }
]);
```

### **4. Запуск и проверка**

```bash
# Подключение через mongosh
mongosh "mongodb+srv://cluster.mongodb.net/" --username your_username

# Или локально
mongosh

# Выполнение скрипта
load("lab5_mongodb.js")

# Проверка коллекций
show collections

# Просмотр документов
db.orders.find().pretty()

# Проверка агрегации
db.orders.aggregate([...])
```

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Полный скрипт вставки данных (users, products, orders)
   - Код агрегационного пайплайна (категории с выручкой)
   - Реализация топ-3 пользователей

2. **Скриншоты:**
   - Результат `db.orders.find().pretty()` для одного заказа (показать вложенную структуру)
   - Результат агрегационного пайплайна по категориям
   - Результат запроса топ-3 пользователей

3. **Ответы на вопросы (сравнение SQL vs NoSQL):**
   - Как в MongoDB представлена связь "заказ-товары" в отличие от PostgreSQL?
   - В каком случае документная модель удобнее реляционной? Приведите пример из работы.
   - Какие операции в MongoDB оказались сложнее/проще по сравнению с SQL?
   - Что такое `$unwind` и зачем он нужен?

### **6. Критерии оценивания:**

#### **Обязательные требования (минимум для зачёта):**
- **Данные:** Вставлены 3 пользователя, 5 продуктов, 3 заказа (каждый с минимум 2 товарами)
- **CRUD:** Корректно выполнены операции READ (с $lookup) и UPDATE (с условием)
- **Агрегация:** Пайплайн с `$unwind`, `$lookup`, `$group`, `$sort` работает и выдаёт верные суммы по категориям

#### **Дополнительные критерии (для повышения оценки):**
- **Сравнение:** Реализованы оба запроса из Части 1 (PostgreSQL) в MongoDB
- **Оптимизация:** Использованы индексы в MongoDB (`createIndex`)
- **Сложный пайплайн:** Добавлены этапы `$facet` или `$bucket` для дополнительной аналитики

#### **Неприемлемые ошибки:**
- Хранение заказов без вложенного массива (реляционный подход в NoSQL)
- Отсутствие `$unwind` при работе с массивами
- Непонимание разницы между `_id` в MongoDB и `id` в PostgreSQL

### **7. Полезные команды для Ubuntu:**

```bash
# Запуск MongoDB Shell
mongosh

# Показать все базы данных
show dbs

# Переключиться на базу
use shop_mongo

# Показать все коллекции
show collections

# Удалить коллекцию
db.orders.drop()

# Создать индекс
db.orders.createIndex({ "user_id": 1 })

# Посмотреть индексы
db.orders.getIndexes()

# Профилирование запросов
db.setProfilingLevel(2)
db.system.profile.find().pretty()
```

### **8. Структура проекта:**

```
lab5_mongodb/
├── init.js              # Создание коллекций и вставка данных
├── queries.js           # CRUD операции и агрегационные пайплайны
├── comparison.js        # Сравнительные запросы (топ-3 пользователей)
├── indexes.js           # Создание индексов
└── report/              # Скриншоты и ответы на вопросы
```

### **9. Советы по выполнению:**

1. **Используйте `pretty()`:** `db.collection.find().pretty()` форматирует вывод для читаемости.
2. **Проверяйте каждый этап агрегации:** Выполняйте пайплайн пошагово, комментируя этапы.
3. **Вложенность — ключевое отличие:** В MongoDB старайтесь хранить связанные данные внутри документа (например, `items` внутри `orders`), чтобы избежать лишних `$lookup`.
4. **Сравнивайте с Частью 1:** Выполните те же бизнес-запросы (выручка по категориям, топ пользователей) в обеих СУБД и проанализируйте синтаксис.

**Примечание:** В задании предоставлено ~70% кода (схема коллекций, примеры документов, шаблоны пайплайнов). Ваша задача — дописать недостающие ~30% (добавление заказов, полный агрегационный пайплайн, операции UPDATE/DELETE, сравнительные запросы).

---

## **Итоговое сравнение для отчёта (Часть 1 vs Часть 2):**

| Характеристика | PostgreSQL | MongoDB |
|----------------|------------|---------|
| Схема | Фиксированная (DDL) | Гибкая (схема по желанию) |
| Связи | FOREIGN KEY | Вложенные документы / ссылки |
| JOIN | `JOIN` между таблицами | `$lookup` или денормализация |
| Агрегация | `GROUP BY` + агрегатные функции | `$group` + `$project` |
| Транзакции | ACID (полная поддержка) | Транзакции только на уровне документа (с версии 4.0 - многодокументные) |
| Индексы | B-Tree, Hash, GIN | Одиночные, составные, текстовые, геопространственные |

Заполните эту таблицу в отчёте на основе вашего опыта выполнения обеих частей.