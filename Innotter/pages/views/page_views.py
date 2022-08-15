from rest_framework.decorators import action

from ..mixins.page_mixins import PageViewSetMixin
from ..models import Page
from ..permissons import (IsActiveUser, IsAdminRole, IsNotBlacklisted,
                          IsOwnerOrReadOnly, IsWelcome)
from ..serializers.page_serializers import PageSerializer
from ..services.page_services import (toggle_follow_request,
                                      toggle_page_is_blocked)


class PageViewSet(PageViewSetMixin):
    serializer_class = PageSerializer
    queryset = Page.objects.all()
    permission_classes = {
        "update": [IsOwnerOrReadOnly, IsActiveUser],
        "follow": [IsNotBlacklisted],
        "unfollow": [IsWelcome],
        "create": [IsActiveUser],
        "retrieve": [IsActiveUser, IsWelcome],
        "destroy": [IsOwnerOrReadOnly, IsActiveUser],
        "list": [IsActiveUser],
        "permablock": [IsAdminRole],
        "unblock": [IsAdminRole],
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_follow(self, request, pk=None):
        toggle_follow_request(view=self, request=request)

    @action(detail=True, methods=["put"])
    def permablock(self, request, pk=None):
        return toggle_page_is_blocked(view=self, request=request)
