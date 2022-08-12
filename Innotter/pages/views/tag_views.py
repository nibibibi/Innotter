from rest_framework import viewsets, permissions
from ..models import Tag
from ..serializers.tag_serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer