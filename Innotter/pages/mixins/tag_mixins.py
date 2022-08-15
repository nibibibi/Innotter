from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from ..permissons import DictionaryPermissionsMixin

class TagViewSetMixin(GenericViewSet, DestroyModelMixin, DictionaryPermissionsMixin,
                      CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    pass
    