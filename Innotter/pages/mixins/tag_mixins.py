from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin, ListModelMixin, RetrieveModelMixin
from ..models import Tag
from ..serializers.tag_serializers import TagSerializer
from ..permissons import IsAdminRole, IsActiveUser, DictionaryPermissionsMixin

class TagViewSetMixin(GenericViewSet, DestroyModelMixin, DictionaryPermissionsMixin,
                      CreateModelMixin, RetrieveModelMixin, ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = {
        'destroy' : [IsAdminRole],
        'create' : [IsActiveUser]
    }
    permission_classes['list'] = permission_classes['create']
    permission_classes['retrieve'] = permission_classes['create']
    