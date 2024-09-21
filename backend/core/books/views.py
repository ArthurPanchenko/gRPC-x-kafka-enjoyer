from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import BookListSerializer, BookFullSerializer
from .models import Book


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookFullSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'all_books'
        books = cache.get(cache_key)

        if not books:
            books = self.get_queryset()
            serializer = self.get_serializer(books, many=True)
            cache.set(cache_key, serializer.data, timeout=600)
        else:
            serializer = self.get_serializer(books, many=True)

        return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete('all_books')  # Очистка кэша
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        cache.delete('all_books')  # Очистка кэша
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        cache.delete('all_books')  # Очистка кэша
        return response
