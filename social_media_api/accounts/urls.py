# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ProfileViewSet
from rest_framework.authtoken import views as drf_auth_views

router = DefaultRouter()
router.register('profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),  # uses ObtainAuthToken
    # alternative direct endpoint: path('api-token-auth/', drf_auth_views.obtain_auth_token),
    path('', include(router.urls)),
]
