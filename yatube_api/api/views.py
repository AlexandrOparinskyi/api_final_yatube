from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from posts.models import Group, Follow, Post
from .serializers import (CommentSerializer, GroupSerializer,
                          PostSerializer, FollowSerializer)
from .permissions import IsAuthorOrReadOnly
from .paginations import StandardResultSetPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = StandardResultSetPagination


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    http_method_names = ['get', 'put', 'patch', 'delete']


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
        """Переопределение создания комментария"""
        serializer.save(
            author=self.request.user,
            post=get_object_or_404(
                Post,
                id=self.kwargs['post_id']
            )
        )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    http_method_names = ['post', 'get']
