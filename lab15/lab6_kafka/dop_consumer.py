class WindowedStatsConsumer(OrderStatsConsumer):
    """Консюмер со скользящим окном для расчёта статистики за последнюю минуту"""
    
    def __init__(self, *args, window_seconds=60, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_seconds = window_seconds
        self.order_timestamps = []  # список (timestamp, order_amount)
    
    def update_stats(self, order):
        # TODO: Добавить заказ с текущим временем
        # TODO: Удалить заказы старше window_seconds
        # TODO: Пересчитать статистику только по заказам в окне
        pass
    
    def cleanup_old_orders(self):
        current_time = datetime.now()
        cutoff_time = current_time.timestamp() - self.window_seconds
        # Удалить заказы старше cutoff_time
        pass

    def run(self, timeout_ms=1000):
        """Запуск консюмера для непрерывного чтения сообщений"""
        logger.info("Starting consumer. Waiting for orders...")
        self.connect()
        
        try:
            for message in self.consumer:
                order = message.value
                logger.info(f"Received order {order['order_id']} from customer {order['customer']['name']}")
                
                self.update_stats(order)
                self.print_stats()
                
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
        finally:
            self.consumer.close()
            self.print_final_report()
    
    def print_final_report(self):
        """Финальный отчёт после остановки консюмера"""
        runtime = datetime.now() - self.stats['start_time']
        logger.info("=" * 50)
        logger.info("ФИНАЛЬНЫЙ ОТЧЁТ")
        logger.info(f"Время работы: {runtime.total_seconds():.2f} секунд")
        logger.info(f"Обработано заказов: {self.stats['total_orders']}")
        logger.info(f"Средняя скорость: {self.stats['total_orders'] / runtime.total_seconds():.2f} заказов/сек")
        logger.info("=" * 50)
if __name__ == "__main__":
    consumer = OrderStatsConsumer()
    consumer.run()