from ..mixins.tag_mixins import TagViewSetMixin
from ..models import Tag
from ..permissons import IsActiveUser, IsAdminRole
from ..serializers.tag_serializers import TagSerializer


class TagViewSet(TagViewSetMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = {
        "destroy": [IsAdminRole],
        "create": [IsActiveUser],
        "retrieve": [IsActiveUser],
        "list": [IsActiveUser]}
