# Advanced Features and Security

- **Custom User Model**: `CustomUser` in `bookshelf/models.py` extends `AbstractUser` with `date_of_birth` and `profile_photo`.
- **Permissions/Groups**: `Book` model defines `can_view`, `can_create`, `can_edit`, `can_delete`. Assign groups in Django admin.
- **Security Best Practices**: Settings configured in `settings.py` (DEBUG False, secure cookies, HTTPS redirect, HSTS).
- **Views**: Use `@permission_required` to restrict actions. Forms include `{% csrf_token %}`.
