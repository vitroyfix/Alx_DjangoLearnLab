from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets

# Simple List APIView
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Full CRUD ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
