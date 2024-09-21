import json
import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Book
from .kafka_producer import send_kafka_message


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Book)
def book_save_signal(sender, instance, created, **kwargs):
    event = 'created' if created else 'updated'
    message = {
        'event': event,
        'book': {
            'id': instance.id,
            'title': instance.title,
            'author': instance.author,
            'publish_date': str(instance.publish_date)
        }
    }

    send_kafka_message('book_events', message)
    logger.info(f'Сообщение отправленно в kafka {message}')

@receiver(post_delete, sender=Book)
def book_delete_signal(sender, instance, **kwargs):
    message = {
        'event': 'deleted',
        'book': {
            'id': instance.id,
            'title': instance.title,
            'author': instance.author,
            'publish_date': str(instance.publish_date)
        }
    }

    send_kafka_message('book_events', message)
    logger.info(f'Сообщение отправленно в kafka {message}')