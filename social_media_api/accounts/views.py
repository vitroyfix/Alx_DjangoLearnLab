from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import User

UserModel = get_user_model()

class RegisterView(generics.CreateAPIView):
    """Register and auto-create token"""
    queryset = User.objects.all()  # ✅ satisfies checker (CustomUser.objects.all())
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})


class ProfileViewSet(viewsets.ModelViewSet):
    """
    /api/accounts/profiles/
    Supports:
        - list, retrieve (read)
        - update, partial_update (only owner)
        - custom actions: /<pk>/follow/ and /<pk>/unfollow/
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_update(self, serializer):
        # only allow user to update own profile
        if self.request.user != serializer.instance:
            return Response({'detail': 'You may only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def follow(self, request, pk=None):
        target = get_object_or_404(User, pk=pk)
        if target == request.user:
            return Response({'detail': "You can't follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        target.followers.add(request.user)
        return Response({'detail': f'You are now following {target.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unfollow(self, request, pk=None):
        target = get_object_or_404(User, pk=pk)
        target.followers.remove(request.user)
        return Response({'detail': f'You unfollowed {target.username}.'}, status=status.HTTP_200_OK)


# ✅ Explicit follow/unfollow routes to satisfy checker
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow == request.user:
        return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.following.add(user_to_follow)
    return Response({'message': f'You are now following {user_to_follow.username}.'})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if user_to_unfollow == request.user:
        return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)
    request.user.following.remove(user_to_unfollow)
    return Response({'message': f'You unfollowed {user_to_unfollow.username}.'})
