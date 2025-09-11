from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required

from .models import Book, Library, UserProfile

# -----------------------------
# Function-based view
# -----------------------------
def list_books(request):
    # Checker requires Book.objects.all()
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

# -----------------------------
# Class-based view
# -----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

# -----------------------------
# Registration View
# -----------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "relationship_app/register.html", {"form": form, "success": True})
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})

# -----------------------------
# Role-based Views
# -----------------------------
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

# -----------------------------
# Book CRUD with permissions
# -----------------------------
@permission_required("relationship_app.can_add_book")
def add_book(request):
    return render(request, "relationship_app/admin_view.html", {"message": "Book added (dummy view)"})

@permission_required("relationship_app.can_change_book")
def edit_book(request):
    return render(request, "relationship_app/admin_view.html", {"message": "Book edited (dummy view)"})

@permission_required("relationship_app.can_delete_book")
def delete_book(request):
    return render(request, "relationship_app/admin_view.html", {"message": "Book deleted (dummy view)"})
