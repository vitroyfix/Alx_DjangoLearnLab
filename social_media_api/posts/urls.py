# posts/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')

# For nested comments you can do a nested route
comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_pk>/comments/', comment_list, name='post-comments'),
    path('posts/<int:post_pk>/comments/<int:pk>/', comment_detail, name='post-comment-detail'),
    path('feed/', FeedView.as_view(), name='feed'),
]
