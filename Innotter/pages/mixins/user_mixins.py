from rest_framework.viewsets import ReadOnlyModelViewSet

from ..permissons import DictionaryPermissionsMixin


class UserViewSetMixin(DictionaryPermissionsMixin, ReadOnlyModelViewSet):
    pass
