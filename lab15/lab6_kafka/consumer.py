"""
Kafka Consumer: Обработка событий заказов и агрегация статистики в реальном времени
"""

from kafka import KafkaConsumer
import json
from collections import defaultdict
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OrderStatsConsumer:
    """Консюмер для агрегации статистики заказов в реальном времени"""
    
    def __init__(self, bootstrap_servers='localhost:9092', topic='orders', group_id='order_stats_group'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        
        # Хранилище агрегированных данных
        self.stats = {
            'total_orders': 0,
            'total_revenue': 0.0,
            'orders_by_category': defaultdict(int),
            'orders_by_city': defaultdict(int),
            'recent_orders': [],  # последние 10 заказов
            'start_time': datetime.now()
        }
        
    def connect(self):
        """Создание подключения к Kafka"""
        # TODO: Создать экземпляр KafkaConsumer с десериализацией JSON
        # Ваш код:
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None
            )
            logger.info(f"Connected to Kafka, subscribed to topic: {self.topic}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    def update_stats(self, order):
        """Обновление статистики на основе полученного заказа"""
        # TODO: Обновить все счетчики в self.stats
        # Ваш код:
        
        # Увеличить общее количество заказов
        self.stats['total_orders'] += 1
        
        # Добавить сумму заказа к общей выручке
        self.stats['total_revenue'] += order['total_amount']
        
        # Обновить статистику по категориям
        for item in order['items']:
            category = item['category']
            self.stats['orders_by_category'][category] += 1
        
        # Обновить статистику по городам
        city = order['customer']['city']
        self.stats['orders_by_city'][city] += 1
        
        # Добавить в список последних заказов (хранить только 10)
        self.stats['recent_orders'].append({
            'order_id': order['order_id'],
            'customer': order['customer']['name'],
            'total': order['total_amount'],
            'time': order['timestamp']
        })
        if len(self.stats['recent_orders']) > 10:
            self.stats['recent_orders'].pop(0)
    
    def print_stats(self):
        """Вывод текущей статистики в консоль"""
        logger.info("=" * 50)
        logger.info(f"ТЕКУЩАЯ СТАТИСТИКА ЗАКАЗОВ")
        logger.info(f"Всего заказов: {self.stats['total_orders']}")
        logger.info(f"Общая выручка: {self.stats['total_revenue']:,.2f} руб.")
        logger.info(f"Средний чек: {self.stats['total_revenue'] / self.stats['total_orders']:,.2f} руб." if self.stats['total_orders'] > 0 else "Средний чек: 0")
        logger.info(f"Заказов по категориям: {dict(self.stats['orders_by_category'])}")
        logger.info(f"Заказов по городам: {dict(self.stats['orders_by_city'])}")
        logger.info(f"Последние 3 заказа: {self.stats['recent_orders'][-3:]}")
        logger.info("=" * 50)
    
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