# posts/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from posts.models import Post as PostModel
from rest_framework.permissions import IsAuthenticated

# Simple PageNumberPagination already configured globally. You can override per-view if needed.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        # simple like toggle using a through model or separate Like model (we'll assume Like model exists)
        from notifications.models import Notification
        from posts.models import Like
        liked, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        # create simple notification
        Notification.objects.create(recipient=post.author, actor=user, verb='liked', target_object=post)
        return Response({'detail': 'Post liked.'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        from posts.models import Like
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            return Response({'detail': 'Unliked.'})
        except Like.DoesNotExist:
            return Response({'detail': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post__pk=self.kwargs.get('post_pk')).order_by('-created_at')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)

# Feed view
from rest_framework.views import APIView
class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        following_qs = user.following.all()  # users this user follows
        posts = Post.objects.filter(author__in=following_qs).order_by('-created_at')
        page = self.request.query_params.get('page')
        paginator = PageNumberPagination()
        paginated = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
