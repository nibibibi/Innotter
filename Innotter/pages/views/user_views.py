from ..permissons import IsAdminRole
from users.models import User
from users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from ..services import user_services


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post',])
    def block(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action='block')
    
    @action(detail=True, methods=['post',])
    def unblock(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action='unblock')
        
        
        
        