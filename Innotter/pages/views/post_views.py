from ssl import DER_cert_to_PEM_cert
from rest_framework.decorators import action

from ...users.models import User
from ..permissons import IsActiveUser, IsAdminRole, IsAlreadyWelcomed, IsAuthorOrReadOnly, IsModeratorRole
from ..models import Post
from ..serializers.post_serializers import PostSerializer
from ..mixins.post_mixins import PostViewSetMixin
from ..services.post_services import toggle_is_favourite


class PostViewSet(PostViewSetMixin):
    permission_classes = {
        'create': [IsAuthorOrReadOnly, IsActiveUser],
        'list': [(IsAdminRole | IsModeratorRole)]
    }
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    @action(detail=True, methods=['get'])
    def favourite(self, request, pk=None):
        return toggle_is_favourite(view=self, request=request)
    
    @action(detail=True, methods=['get'])
    def unfavourite(self, request, pk=None):
        return toggle_is_favourite(view=self,request=request)