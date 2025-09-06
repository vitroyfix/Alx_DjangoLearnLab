from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Book, Library
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})

# Class-based view: Library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"
# Register view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})

# Logout view
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.profile.role == "Admin"

def is_librarian(user):
    return user.is_authenticated and user.profile.role == "Librarian"

def is_member(user):
    return user.is_authenticated and user.profile.role == "Member"

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "member_view.html")
@permission_required("relationship_app.can_add_book")
def add_book(request):
    return HttpResponse("Book added successfully.")

@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Editing book: {book.title}")

@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Deleted book: {book.title}")