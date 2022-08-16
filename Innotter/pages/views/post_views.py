from rest_framework.decorators import action
from rest_framework.response import Response
from ..mixins.post_mixins import PostViewSetMixin
from ..models import Post
from ..permissons import (
    IsActiveUser,
    IsAdminRole,
    IsAuthorOrReadOnly,
    IsModeratorRole,
)
from ..serializers.post_serializers import PostSerializer
from ..services.post_services import toggle_is_favourite


class PostViewSet(PostViewSetMixin):
    permission_classes = {
        "create": [IsAuthorOrReadOnly, IsActiveUser],
        "list": [(IsAdminRole | IsModeratorRole | IsActiveUser)],
        "favourite": [IsActiveUser],
        "destroy": [(IsAdminRole | IsModeratorRole)],
    }
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["get"])
    def toggle_favourite(self, request, pk=None):
        message = toggle_is_favourite(view=self, request=request)
        return Response(message, status=200)
