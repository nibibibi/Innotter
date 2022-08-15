from ..mixins.user_mixins import UserViewSetMixin
from rest_framework.decorators import action
from ..services import user_services
from ..permissons import IsActiveUser, IsAdminRole
from users.models import User
from users.serializers import UserSerializer
from ..serializers.user_serializers import UserFavouritePostsSerializer
from django.http import JsonResponse


class UserViewSet(UserViewSetMixin):
    permission_classes = {
        'block': [IsAdminRole],
        'unblock': [IsAdminRole],
        "list_favourites": [IsActiveUser]
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post',])
    def block(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action=self.action)
    
    @action(detail=True, methods=['post',])
    def unblock(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action=self.action)
    
    @action(detail=False, methods=['get'])
    def list_favourites(self, request):
        return JsonResponse(UserFavouritePostsSerializer(request.user).data, status=200)
        
