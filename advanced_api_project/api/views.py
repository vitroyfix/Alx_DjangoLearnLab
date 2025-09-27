from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class BookListView(generics.ListAPIView):
    """List books with filtering, searching, and ordering"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtering by fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Searching by fields
    search_fields = ['title', 'author__name']

    # Ordering options
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering
