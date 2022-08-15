from rest_framework import viewsets
from ..permissons import DictionaryPermissionsMixin


class PageViewSetMixin(DictionaryPermissionsMixin, viewsets.GenericViewSet):
    pass