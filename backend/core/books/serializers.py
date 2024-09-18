from rest_framework import serializers

from .models import Book


class BookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'id',
            'title',
        )


class BookFullSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'id', 
            'title',
            'author',
            'publish_date'
        )