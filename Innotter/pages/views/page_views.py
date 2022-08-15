from rest_framework.decorators import action

from ..mixins.page_mixins import PageViewSetMixin
from ..models import Page
from ..permissons import (
    IsActiveUser,
    IsAdminRole,
    IsModeratorRole,
    IsNotBlacklisted,
    IsOwnerOrReadOnly,
    IsWelcome,
)
from ..serializers.page_serializers import (
    EditPageSerializer,
    ListRequestsPageSerializer,
    PageSerializer,
    TimeBlockPageSerializer,
    ToggleFollowRequestPageSerializer,
    ToggleTagPageSerializer,
)
from ..services.page_services import (
    accept_follow_request,
    reject_all_follow_requests,
    reject_follow_request,
    toggle_follow_request,
    toggle_page_is_private,
    toggle_page_permamently_blocked,
    toggle_page_tag,
)


class PageViewSet(PageViewSetMixin):
    queryset = Page.objects.all()
    permission_classes = {
        "update": [IsOwnerOrReadOnly, IsActiveUser],
        "timeblock": [(IsAdminRole | IsModeratorRole)],
        "toggle_follow": [IsNotBlacklisted],
        "create": [IsActiveUser],
        "retrieve": [IsActiveUser, IsWelcome],
        "destroy": [IsOwnerOrReadOnly, IsActiveUser],
        "list": [IsAdminRole],
        "toggle_permablock": [IsAdminRole],
        "toggle_is_private": [IsOwnerOrReadOnly],
        "toggle_tag": [IsOwnerOrReadOnly],
    }
    serializer_classes = {
        "timeblock": TimeBlockPageSerializer,
        "default": PageSerializer,
        "list_requests": ListRequestsPageSerializer,
        "accept": ToggleFollowRequestPageSerializer,
        "reject": ToggleFollowRequestPageSerializer,
        "update": EditPageSerializer,
        "toggle_tag": ToggleTagPageSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle_permablock(self, request, pk=None):
        return toggle_page_permamently_blocked(view=self, request=request)

    @action(detail=True, methods=["post"])
    def toggle_follow(self, request, pk=None):
        return toggle_follow_request(view=self, request=request)

    @action(detail=True, methods=["put"])
    def timeblock(self, request, pk=None):
        return super().partial_update(request=request)

    @action(detail=True, methods="get")
    def list_requests(self, request, pk=None):
        return super().retrieve(request=request)

    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):
        return accept_follow_request(view=self, request=request)

    @action(detail=True, methods="post")
    def reject(self, request, pk=None):
        return reject_follow_request(view=self, request=request)

    @action(detail=True, methods=["post"])
    def reject_all(self, request, pk=None):
        return reject_all_follow_requests(view=self, request=request)

    @action(detail=True, methods=["post"])
    def toggle_is_priavte(self, request, pk=None):
        return toggle_page_is_private(view=self, request=request)

    @action(detail=True, methods=["post"])
    def toggle_tag(self, request, pk=None):
        return toggle_page_tag(view=self, request=request)

    def get_serializer_class(
        self,
    ):  # TODO: refactor to smth i dunno how it should look ahh whatever i'm hungry already even though i just ate in krasavik cafe btw my pass doesn't work in restaurant for some reason # TODO: delete previous comment # TODO: and next one too ( wait is it an infinite recursion? )
        return (
            self.serializer_classes[self.action]
            if self.action in self.serializer_classes
            else self.serializer_classes["default"]
        )
