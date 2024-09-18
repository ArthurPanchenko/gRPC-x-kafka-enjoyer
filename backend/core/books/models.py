from django.db import models


class Book(models.Model):
    '''Модель книги (id, title, author, publish_date)'''

    title = models.CharField('Название', max_length=255)
    author = models.CharField('Автор', max_length=255)
    publish_date = models.DateField('Дата публикации')

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title
