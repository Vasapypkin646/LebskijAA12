# **Лабораторная работа 15. Часть 2: Знакомство с Apache Kafka**

## **Тема:** Потоковая обработка данных: архитектура Apache Kafka, продюсеры, консюмеры и сценарии использования.

### **Цель работы:**
Получить практические навыки работы с Apache Kafka: запуск кластера через Docker Compose, создание топиков, написание продюсера и консюмера для потоковой передачи сообщений, анализ сценариев использования потоковой обработки.

---

## **Задание: Разработка системы потоковой передачи событий интернет-магазина**

Вам необходимо развернуть Apache Kafka, создать топик для событий заказов, реализовать продюсера, который генерирует события о новых заказах, и консюмера, который обрабатывает эти события (агрегирует статистику в реальном времени).

### **1. Настройка проекта**

Установите Docker и Docker Compose, создайте конфигурацию для запуска Kafka.

```bash
# Создание директории проекта
mkdir lab6_kafka && cd lab6_kafka

# Установка Docker (если не установлен)
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker

# Добавление пользователя в группу docker (чтобы не использовать sudo)
sudo usermod -aG docker $USER
# Выйдите и зайдите заново или выполните: newgrp docker

# Проверка установки
docker --version
docker-compose --version
```

**Файл: `docker-compose.yml`**

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"
    networks:
      - kafka-network

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
    networks:
      - kafka-network

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    container_name: kafka-ui
    depends_on:
      - kafka
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181
    ports:
      - "8080:8080"
    networks:
      - kafka-network

networks:
  kafka-network:
    driver: bridge
```

### **2. Базовый код (70% предоставляется)**

**Файл: `producer.py` (продюсер событий)**

```python
"""
Kafka Producer: Генерация событий о заказах интернет-магазина
"""

from kafka import KafkaProducer
import json
import random
import time
import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OrderEventProducer:
    """Продюсер событий заказов в Kafka"""
    
    def __init__(self, bootstrap_servers='localhost:9092', topic='orders'):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        
    def connect(self):
        """Создание подключения к Kafka"""
        # TODO: Создать экземпляр KafkaProducer с сериализацией JSON
        # Ваш код:
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            logger.info(f"Connected to Kafka at {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    def generate_order(self):
        """Генерация случайного заказа"""
        products = [
            {"product_id": 1, "name": "Ноутбук", "price": 75000, "category": "Электроника"},
            {"product_id": 2, "name": "Мышь", "price": 1500, "category": "Электроника"},
            {"product_id": 3, "name": "Книга SQL", "price": 2500, "category": "Книги"},
            {"product_id": 4, "name": "Клавиатура", "price": 5000, "category": "Электроника"},
            {"product_id": 5, "name": "Монитор", "price": 25000, "category": "Электроника"},
            {"product_id": 6, "name": "Книга Python", "price": 3500, "category": "Книги"}
        ]
        
        customers = [
            {"id": 1, "name": "Анна Смирнова", "city": "Москва"},
            {"id": 2, "name": "Петр Иванов", "city": "СПб"},
            {"id": 3, "name": "Мария Сидорова", "city": "Казань"},
            {"id": 4, "name": "Иван Петров", "city": "Москва"},
            {"id": 5, "name": "Елена Козлова", "city": "Новосибирск"}
        ]
        
        product = random.choice(products)
        customer = random.choice(customers)
        quantity = random.randint(1, 3)
        
        order = {
            "order_id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "customer": customer,
            "items": [{
                "product_id": product["product_id"],
                "product_name": product["name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": product["price"],
                "total_price": quantity * product["price"]
            }],
            "total_amount": quantity * product["price"],
            "payment_method": random.choice(["card", "cash", "online"])
        }
        
        return order
    
    def send_order(self, order):
        """Отправка одного заказа в Kafka"""
        # TODO: Отправить сообщение в топик с ключом = customer_id
        # Ваш код:
        key = str(order['customer']['id'])
        future = self.producer.send(self.topic, key=key, value=order)
        
        # Ожидание подтверждения
        try:
            record_metadata = future.get(timeout=10)
            logger.info(f"Order {order['order_id']} sent to partition {record_metadata.partition} at offset {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Failed to send order: {e}")
        
        return future
    
    def run(self, interval_seconds=2, max_orders=10):
        """Запуск генерации и отправки заказов"""
        logger.info(f"Starting producer. Sending {max_orders} orders every {interval_seconds}s")
        
        self.connect()
        
        for i in range(max_orders):
            order = self.generate_order()
            self.send_order(order)
            time.sleep(interval_seconds)
        
        # Ожидание завершения всех отправок
        self.producer.flush()
        logger.info("All orders sent successfully")
        self.producer.close()


if __name__ == "__main__":
    producer = OrderEventProducer()
    producer.run(interval_seconds=1, max_orders=15)
```

**Файл: `consumer.py` (консюмер событий)**

```python
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
```

### **3. Задания для самостоятельного выполнения (30% дописать)**

#### **A. Запуск Kafka кластера через Docker Compose** (обязательно)

Выполните команды для запуска и проверки работоспособности Kafka.

```bash
# Запуск всех сервисов (Zookeeper, Kafka, Kafka-UI)
docker-compose up -d

# Проверка статуса контейнеров
docker-compose ps

# Просмотр логов Kafka
docker-compose logs kafka

# Проверка создания топика (если не создан автоматически)
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Создание топика 'orders' (если он не создался автоматически)
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 \
  --create --topic orders --partitions 3 --replication-factor 1

# Описание топика (просмотр партиций)
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 \
  --describe --topic orders
```

#### **B. Установка Python библиотеки для Kafka** (обязательно)

```bash
# Активация виртуального окружения (если используете)
python3 -m venv venv
source venv/bin/activate

# Установка kafka-python
pip install kafka-python

# Дополнительные библиотеки для продвинутой работы
pip install confluent-kafka  # альтернативная библиотека (более производительная)
```

#### **C. Реализация методов `connect()` в продюсере и консюмере** (обязательно)

Допишите недостающий код в `producer.py` и `consumer.py`:

**Для продюсера (`producer.py`):**
```python
def connect(self):
    self.producer = KafkaProducer(
        bootstrap_servers=self.bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all',  # подтверждение от всех реплик
        retries=3
    )
```

**Для консюмера (`consumer.py`):**
```python
def connect(self):
    self.consumer = KafkaConsumer(
        self.topic,
        bootstrap_servers=self.bootstrap_servers,
        group_id=self.group_id,
        auto_offset_reset='earliest',  # начать с самых старых сообщений
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        key_deserializer=lambda k: k.decode('utf-8') if k else None
    )
```

#### **D. Реализация метода `update_stats()` в консюмере** (обязательно)

Допишите полную логику обновления статистики:

```python
def update_stats(self, order):
    # Увеличить общее количество заказов
    self.stats['total_orders'] += 1
    
    # Добавить сумму заказа к общей выручке
    self.stats['total_revenue'] += order['total_amount']
    
    # Обновить статистику по категориям (проход по items)
    for item in order['items']:
        category = item['category']
        self.stats['orders_by_category'][category] += 1
    
    # Обновить статистику по городам
    city = order['customer']['city']
    self.stats['orders_by_city'][city] += 1
    
    # Добавить в список последних заказов
    self.stats['recent_orders'].append({
        'order_id': order['order_id'],
        'customer': order['customer']['name'],
        'total': order['total_amount'],
        'time': order['timestamp']
    })
    
    # Ограничить список 10 элементами
    if len(self.stats['recent_orders']) > 10:
        self.stats['recent_orders'].pop(0)
```

#### **E. Создание дополнительного консюмера для агрегации по окну времени** (дополнительно)

Реализуйте консюмера, который считает статистику за последние 60 секунд (sliding window):

```python
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
```

### **4. Запуск и проверка**

```bash
# Терминал 1: Запуск Kafka инфраструктуры
docker-compose up -d

# Терминал 2: Запуск консюмера (слушаем события)
python consumer.py

# Терминал 3: Запуск продюсера (генерируем заказы)
python producer.py

# Просмотр веб-интерфейса Kafka UI
# Открыть браузер: http://localhost:8080

# Проверка через командную строку Kafka
docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic orders --from-beginning

# Остановка всех сервисов
docker-compose down

# Остановка с удалением томов (очистка данных)
docker-compose down -v
```

### **5. Что должно быть в отчёте:**

1. **Исходный код:**
   - Полный код `producer.py` и `consumer.py` с реализованными методами
   - Конфигурация `docker-compose.yml`

2. **Скриншоты:**
   - Вывод консюмера с обновляющейся статистикой (минимум 5 заказов)
   - Скриншот Kafka UI с отображением топика `orders` и партиций
   - Вывод команды `docker-compose ps` с работающими контейнерами

3. **Ответы на вопросы:**
   - Что такое топик, партиция, оффсет в Kafka? Как они использовались в работе?
   - В чём разница между продюсером и консюмером? Зачем нужна группа консюмеров (`group_id`)?
   - Какие преимущества даёт потоковая обработка перед пакетной (ETL из Части 1)?
   - Приведите 3 реальных сценария использования Kafka в бизнесе (не связанных с логированием).
   - Что произойдёт, если запустить 2 консюмера с одинаковым `group_id`?

### **6. Критерии оценивания:**

#### **Обязательные требования (минимум для зачёта):**
- **Docker Compose:** Все 3 сервиса (Zookeeper, Kafka, Kafka-UI) успешно запущены
- **Продюсер:** Корректно подключается к Kafka и отправляет сообщения (логи с подтверждением)
- **Консюмер:** Корректно читает сообщения и обновляет статистику (total_orders, total_revenue)

#### **Дополнительные критерии (для повышения оценки):**
- **Партиционирование:** Продюсер использует ключ (`customer_id`) для отправки в конкретную партицию
- **Обработка ошибок:** Реализованы повторные попытки (retries) при отправке сообщений
- **Windowed consumer:** Реализован консюмер со скользящим окном (задание E)
- **Мониторинг:** Использован Kafka UI для проверки состояния топика

#### **Неприемлемые ошибки:**
- Консюмер не читает сообщения (неправильная настройка `group_id` или `auto_offset_reset`)
- Отсутствие сериализации/десериализации JSON (сообщения приходят как bytes)
- Продюсер не обрабатывает исключения при недоступности Kafka

### **7. Полезные команды для Ubuntu:**

```bash
# Просмотр всех топиков
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list

# Удаление топика
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 \
  --delete --topic orders

# Просмотр оффсетов для топика
docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group order_stats_group --describe

# Мониторинг задержки (lag) консюмера
docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group order_stats_group --describe

# Просмотр логов контейнера в реальном времени
docker-compose logs -f kafka

# Проверка использования ресурсов
docker stats

# Очистка всех неиспользуемых контейнеров и образов
docker system prune -a
```

### **8. Структура проекта:**

```
lab6_kafka/
├── docker-compose.yml        # Конфигурация Kafka кластера
├── producer.py               # Генератор событий заказов
├── consumer.py               # Агрегатор статистики
├── windowed_consumer.py      # Дополнительный консюмер с окном
├── requirements.txt          # Зависимости (kafka-python)
├── data/
│   └── orders_processed.json # Сохранённая статистика (опционально)
└── report/
    ├── screenshots/          # Скриншоты выполнения
    └── answers.md            # Ответы на вопросы
```

### **9. Советы по выполнению:**

1. **Запускайте в правильном порядке:** Сначала `docker-compose up -d`, дождитесь инициализации Kafka (около 30 секунд), затем продюсер и консюмер.

2. **Проверьте подключение:** Если продюсер не может подключиться, проверьте `bootstrap_servers='localhost:9092'` и что контейнер Kafka действительно слушает на этом порту:
   ```bash
   netstat -tulpn | grep 9092
   ```

3. **Используйте несколько терминалов:** Это облегчит отладку — в одном терминале логи контейнеров, в другом консюмер, в третьем продюсер.

4. **Для больших объёмов данных:** Увеличьте `max_orders` в продюсере до 1000 и наблюдайте, как консюмер обрабатывает поток.

5. **Экспериментируйте с партициями:** Измените количество партиций в топике и посмотрите, как сообщения распределяются:
   ```bash
   docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 \
     --alter --topic orders --partitions 6
   ```

6. **Сравнение с Частью 1 (ETL):** Отметьте в отчёте ключевые отличия:
   - ETL: пакетная обработка, задержка от минут до часов
   - Kafka: потоковая обработка, задержка в миллисекундах
   - ETL: подходит для отчётов и аналитики
   - Kafka: подходит для мониторинга, уведомлений, реального времени

**Примечание:** В задании предоставлено ~70% кода (структура продюсера и консюмера, генерация данных, базовые методы). Ваша задача — реализовать подключение к Kafka и логику обновления статистики (помечены `TODO`).

---

## **Итоговое сравнение для отчёта (Часть 1 vs Часть 2 лабораторной работы 6):**

| Характеристика | ETL (Python + SQLite) | Потоковая обработка (Kafka) |
|----------------|------------------------|------------------------------|
| Тип обработки | Пакетная (batch) | Потоковая (streaming) |
| Задержка | Минуты/часы | Миллисекунды/секунды |
| Хранение состояний | В SQLite (диск) | В памяти консюмера |
| Масштабирование | Вертикальное (мощнее сервер) | Горизонтальное (больше партиций) |
| Отказоустойчивость | Низкая (один скрипт) | Высокая (репликация Kafka) |
| Сложность | Низкая | Средняя |
| Use cases | Ежедневные отчёты, дашборды | Мониторинг, алерты, real-time analytics |

Добавьте эту таблицу в отчёт с вашими наблюдениями после выполнения обеих частей.
