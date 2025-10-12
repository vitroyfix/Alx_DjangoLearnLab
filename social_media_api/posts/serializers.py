from rest_framework import serializers
from .models import Post, Comment, Like
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','profile_picture')

class CommentSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','post','author','content','created_at','updated_at')
        read_only_fields = ('author','created_at','updated_at','post')

class PostSerializer(serializers.ModelSerializer):
    author = UserBasicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Post
        fields = ('id','author','title','content','created_at','updated_at','comments','likes_count')
        read_only_fields = ('author','created_at','updated_at','comments','likes_count')
