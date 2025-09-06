from django.urls import path
from . import views

urlpatterns = [
    # Function-based
    path("books/", views.list_books, name="list_books"),

    # Class-based
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # CRUD with permissions
    path("add-book/", views.add_book, name="add_book"),
    path("edit-book/", views.edit_book, name="edit_book"),
    path("delete-book/", views.delete_book, name="delete_book"),
]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Function-based
    path("books/", views.list_books, name="list_books"),

    # Class-based
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),

    # Authentication (use built-in directly with template_name)
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),

    # Role-based
    path("admin-view/", views.admin_view, name="admin_view"),
    path("librarian-view/", views.librarian_view, name="librarian_view"),
    path("member-view/", views.member_view, name="member_view"),

    # CRUD with permissions
    path("add-book/", views.add_book, name="add_book"),
    path("edit-book/", views.edit_book, name="edit_book"),
    path("delete-book/", views.delete_book, name="delete_book"),
]
