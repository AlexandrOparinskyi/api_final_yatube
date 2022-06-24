from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from posts.models import Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        return False


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    def get_queryset(self):
        """Создание queryset комментария"""
        post = get_object_or_404(
            Post,
            id=self.kwargs['post_id']
        )
        return post.comments.filter(post_id=post)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(
                Post,
                id=self.kwargs['post_id']
            )
        )
