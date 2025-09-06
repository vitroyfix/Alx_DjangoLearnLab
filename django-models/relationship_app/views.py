from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "list_books.html", {"books": books})

# Class-based view: display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "library_detail.html"
    context_object_name = "library"
# User registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# User login
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

# User logout
def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return hasattr(user, "profile") and user.profile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "profile") and user.profile.role == "Librarian"

def is_member(user):
    return hasattr(user, "profile") and user.profile.role == "Member"

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
    return render(request, "add_book.html")

@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    return render(request, "edit_book.html", {"book_id": book_id})

@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    return render(request, "delete_book.html", {"book_id": book_id})