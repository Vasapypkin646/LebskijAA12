// Переключение на базу данных

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
    },
    {
        _id: 4,
        name: "Книга SQL",
        category: "Книги",
        price: 1000,
        stock_quantity: 60,
        specs: {
            author: "Aдитья Б.",
            pages: 450
        }
    },
    {
        _id: 5,
        name: "USB флешка",
        category: "Электроника",
        price: 500,
        stock_quantity: 100,
        
    }
]);

// TODO: Добавьте ещё 2 продукта самостоятельно (см. задание A)
// TODO: Создайте заказы (каждый заказ содержит массив товаров)
db.orders.insertMany([
    {
        _id: 1,
        user_id: 1,  // Alice
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 1, quantity: 1, price: 75000 },  // Ноутбук
            { product_id: 2, quantity: 2, price: 1500 },    // Мышь x2
            { product_id: 5, quantity: 1, price: 500}
        ]
    },
    {
        _id: 2,
        user_id: 2,  // Bob
        order_date: new Date(),
        status: "completed",
        items: [
            { product_id: 3, quantity: 1, price: 2500 },    // Книга SQL
            { product_id: 4, quantity: 1, price: 1000}
        ]
    },
    // TODO: добавьте третий заказ (любой)
    {
        _id: 3,
        user_id: 2,
        oeder_date: new Date(),
        status: "pending",
        items: [
            { product_id: 5, quantity: 2, price: 500}
        ]
    }
]);