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


db.orders.updateMany(
    {},  // все заказы
    [
        {
            $set: {
                total_amount: {
                    $sum: {
                        $map: {
                            input: "$items",
                            as: "item",
                            in: { $multiply: ["$$item.quantity", "$$item.price"] }
                        }
                    }
                }
            }
        }
    ]
);

db.orders.updateMany(
    { total_amount: { $gt: 8000 } },
    { $set: { discount: 10 } }
);

// TODO: Вычислите дату 30 дней назад и удалите отменённые заказы
// Ваш код:
const thirtyDaysAgo = new Date();
thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

db.orders.deleteMany({
    status: "cancelled",
    order_date: { $lt: thirtyDaysAgo },
    
});
