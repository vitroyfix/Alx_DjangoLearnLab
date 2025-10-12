# social_media_api

Starter Social Media REST API (Django + DRF)

## Setup (local)

1. Create venv and install packages:

2. Configure `social_media_api/settings.py`:
- Set `AUTH_USER_MODEL = 'accounts.User'`
- Add `rest_framework`, `rest_framework.authtoken`, `accounts`, `posts`, `notifications` to `INSTALLED_APPS`

3. Migrate:

4. Run:

## Endpoints (examples)

**Register**
POST `/api/accounts/register/`
Body (JSON):
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "supersecret"
}
{ "username": "alice", "password": "supersecret" }
{ "token": "<token>", "user_id": 1, "username": "alice" }
{ "title": "Hello", "content": "My first post" }

---

# 17) Additional notes & next steps

- I purposely kept things modular: `ProfileViewSet` for user profile management and follow actions, `PostViewSet` + `CommentViewSet` for posts/comments.
- Notifications use GenericForeignKey so they can point to posts, comments or other targets.
- Pagination is configured globally; change `PAGE_SIZE` as desired or use `LimitOffsetPagination`.
- For production: set `DEBUG=False`, add proper `ALLOWED_HOSTS`, use Postgres, configure static & media files (S3), add HTTPS settings, configure Gunicorn + Nginx, and secure secret keys using environment variables.
- Add tests (DRF’s APITestCase) and Postman collection to document endpoints.
- Consider adding serializers for follow counts, follower lists, and `is_following` boolean in user serializer for UX.

---

# What I didn’t do (but recommend you add)
- Full automated tests (unit + integration).
- File storage backends for production (S3).
- Rate-limiting, throttling, or background tasks for heavy notifications (Celery).
- Email verification on registration.
- Swagger / OpenAPI docs (drf-yasg or drf-spectacular).

---

If you want, I can:
- Produce exact full file contents you can copy/paste into files (I can produce them in this chat).
- Create a `requirements.txt` and a sample `.env` + `Procfile` for Heroku.
- Create a Postman collection (JSON) for the endpoints.
- Write unit tests for the main endpoints.

Which of those would you like next?
