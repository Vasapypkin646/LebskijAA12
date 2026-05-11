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
    {
        $group: {
            _id: "$product_info.category",
            summ_sell: {
                $sum: {
                    $multiply: ["$items.price", "$items.quantity"]
                } 
            }
        },
        

    },
    // TODO: Шаг 4 - Сортировка по выручке
    {
        $sort: {
                summ_sell: -1
            },
            
           
    },
    // TODO: Шаг 5 - Проекция (переименование полей)
    {
         $project: {
                //Категория: "$_id",
                Общая_выручка: "$summ_sell"

            }
    }
]);