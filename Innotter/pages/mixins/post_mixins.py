from rest_framework import viewsets

from ..permissons import DictionaryPermissionsMixin


class PostViewSetMixin(DictionaryPermissionsMixin, viewsets.ModelViewSet):
    pass
