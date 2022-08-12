from rest_framework import viewsets
from ..serializers.page_serializers import PageSerializer
from ..models import Page
from ..permissons import DictionaryPermissionsMixin, IsNotBlacklisted, IsWelcome


class PageViewSetMixin(DictionaryPermissionsMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = {
        'follow': [IsNotBlacklisted],
        'unfollow': [IsWelcome]
    }
    