from django.urls import reverse
from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from .models import Book


User = get_user_model()


class BookViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Создаем пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Получаем JWT токен
        response = self.client.post('/api/v1/token/', {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Создаем книгу для тестов
        self.book = Book.objects.create(title='Test Book', author='Test Author', publish_date='2024-01-01')

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'publish_date': '2024-01-01'
        }
        response = self.client.post('/api/v1/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        for key in data.keys():
            self.assertEqual(response.data[key], data[key])

    def test_update_book(self):
        new_data = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'publish_date': '2024-01-01'
        }
        response = self.client.put(f'/api/v1/books/{self.book.id}/', new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in new_data.keys():
            self.assertEqual(response.data[key], new_data[key])

    def test_destroy_book(self):
        response = self.client.delete(f'/api/v1/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_books(self):
        response = self.client.get('/api/v1/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cache_books(self):
        url = reverse('book-list')
        response = self.client.get(url)

        # Проверяем, что кэш работает
        cache_key = 'all_books'
        cached_books = cache.get(cache_key)
        self.assertIsNotNone(cached_books)
