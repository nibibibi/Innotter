from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet

from ..permissons import DictionaryPermissionsMixin


class TagViewSetMixin(
    GenericViewSet,
    DestroyModelMixin,
    DictionaryPermissionsMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    pass
