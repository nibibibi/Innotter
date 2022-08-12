from ..permissons import IsAdminRole
from users.models import User
from users.serializers import UserSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet


class UserViewSetMixin(ReadOnlyModelViewSet):
    permission_classes = [IsAdminRole,]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    