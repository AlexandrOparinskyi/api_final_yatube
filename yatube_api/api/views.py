from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, permissions

from posts.models import Group, Post
from .paginations import StandardResultSetPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer,
                          PostSerializer, FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    pagination_class = StandardResultSetPagination

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    serializer_class = FollowSerializer
    http_method_names = ['post', 'get']
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        """Переопределения создания queryset"""
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Переопределения создания подписки"""
        serializer.save(
            user=self.request.user
        )
