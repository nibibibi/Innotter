from ..permissons import IsWelcome, IsOwnerOrReadOnly
from ..models import Page
from ..serializers import PageSerializer
from rest_framework import viewsets


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsWelcome, IsOwnerOrReadOnly]
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)