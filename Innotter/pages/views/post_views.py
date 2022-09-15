from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
        "favourite": [IsActiveUser],
        "create": [IsAuthorOrReadOnly, IsActiveUser],
        "list": [(IsAdminRole | IsModeratorRole | IsActiveUser)],
        "retrieve": [IsActiveUser, IsAuthorOrReadOnly],
        "destroy": [(IsAdminRole | IsModeratorRole)],
    }
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=["post"])
    def favourite(self, request, pk=None):
        message = toggle_is_favourite(view=self, request=request)
        return Response(message, status=200)
