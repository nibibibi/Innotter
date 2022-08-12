from ..permissons import IsAdminRole
from users.models import User
from users.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.decorators import action


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        