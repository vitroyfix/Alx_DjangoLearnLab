# Delete Operation
>>> book = Book.objects.get(title="Nineteen Eighty-Four")
>>> book.delete()
# Output: (1, {'bookshelf.Book': 1})
