from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """Serializer for Book model with custom validation"""

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure year is not in the future"""
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for Author that nests related books"""
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
