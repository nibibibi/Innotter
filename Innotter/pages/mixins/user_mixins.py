from ..permissons import DictionaryPermissionsMixin
from rest_framework.viewsets import ReadOnlyModelViewSet


class UserViewSetMixin(DictionaryPermissionsMixin, ReadOnlyModelViewSet):
    pass
    