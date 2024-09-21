import json
import logging
from kafka import KafkaConsumer
from threading import Thread


class KafkaBookConsumer(Thread):
    def __init__(self, topic, bootstrap_servers):
        super().__init__()

        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def run(self):
        for message in self.consumer:
            self.logging_message(message.value)

    def logging_message(self, message):
        event_type = message.get('event')
        book_info = message.get('book')
        
        if event_type and book_info:
            book_id = book_info.get('id')
            title = book_info.get('title')
            author = book_info.get('author')
            publish_date = book_info.get('publish_date')

            log_message = f"Книга {event_type}: ID: {book_id}, Название: {title}, Автор: {author}, Дата публикации: {publish_date}"
            logging.info(log_message)