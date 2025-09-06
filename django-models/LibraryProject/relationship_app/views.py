from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.utils.decorators import method_decorator

from .models import Book, Library


# Function-based view: List all books
def list_books(request):
    books = Book.objects.select_related("author").all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: Library details
@method_decorator(login_required, name="dispatch")
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------------- AUTHENTICATION ----------------
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


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- ROLE-BASED VIEWS ----------------
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# ---------------- PERMISSION-BASED BOOK VIEWS ----------------
@permission_required("relationship_app.can_add_book")
def add_book(request):
    return render(request, "relationship_app/permission_result.html", {"action": "Add Book"})


@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "relationship_app/permission_result.html", {"action": f"Edit {book.title}"})


@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "relationship_app/permission_result.html", {"action": f"Delete {book.title}"})
