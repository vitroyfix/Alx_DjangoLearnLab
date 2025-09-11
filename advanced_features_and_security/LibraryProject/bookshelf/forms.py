# LibraryProject/bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    """Example form for Book model."""
    class Meta:
        model = Book
        fields = ['title', 'author']
