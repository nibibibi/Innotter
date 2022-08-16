from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers import UserSerializer

from ..mixins.user_mixins import UserViewSetMixin
from ..permissons import IsActiveUser, IsAdminRole
from ..serializers.user_serializers import UserFavouritePostsSerializer
from ..services import user_services


class UserViewSet(UserViewSetMixin):
    permission_classes = {
        "toggle_block": [IsAdminRole],
        "list_favourites": [IsActiveUser],
        "retrieve": [IsAdminRole],
        "list": [IsAdminRole],
    }
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def toggle_block(self, request, pk=None):
        message = user_services.toggle_block_unblock(view=self)
        return Response(message, status=200)

    @action(detail=False, methods=["get"])
    def list_favourites(self, request):
        return JsonResponse(UserFavouritePostsSerializer(request.user).data, status=200)
