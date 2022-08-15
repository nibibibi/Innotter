from rest_framework.viewsets import ModelViewSet

from ..permissons import DictionaryPermissionsMixin


class TagViewSetMixin(DictionaryPermissionsMixin, ModelViewSet):
    pass
