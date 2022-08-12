from rest_framework import viewsets
from ..serializers.page_serializers import PageSerializer
from ..models import Page
from ..permissons import IsWelcome, IsOwnerOrReadOnly


class PageViewSetMixin(viewsets.GenericViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = [IsWelcome, IsOwnerOrReadOnly]