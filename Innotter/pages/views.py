from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models, permissons, serializers


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissons.IsWelcome, permissons.IsOwnerOrReadOnly]
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissons.IsAuthorOrReadOnly, permissons.IsAlreadyWelcomed]
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
