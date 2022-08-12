from ..permissons import IsAdminRole
from users.models import User
from users.serializers import UserSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    serializer_class = UserSerializer