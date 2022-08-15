from rest_framework.decorators import action

from ..mixins.page_mixins import PageViewSetMixin
from ..models import Page
from ..permissons import (IsActiveUser, IsAdminRole, IsModeratorRole, IsNotBlacklisted,
                          IsOwnerOrReadOnly, IsWelcome)
from ..serializers.page_serializers import PageSerializer, TimeBlockPageSerializer
from ..services.page_services import (toggle_follow_request,
                                      toggle_page_permamently_blocked)


class PageViewSet(PageViewSetMixin):
    queryset = Page.objects.all()
    permission_classes = {
        'update': [IsOwnerOrReadOnly, IsActiveUser],
        'timeblock': [(IsAdminRole | IsModeratorRole)],
        'toggle_follow': [IsNotBlacklisted],
        'create': [IsActiveUser],
        'retrieve': [IsActiveUser, IsWelcome],
        'destroy': [IsOwnerOrReadOnly, IsActiveUser],
        'list': [IsAdminRole],
        'toggle_permablock': [IsAdminRole],
    }
    serializer_classes = {
        'timeblock': TimeBlockPageSerializer,
        'default': PageSerializer,
    }

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_permablock(self, request, pk=None):
        return toggle_page_permamently_blocked(view=self, request=request)

    @action(detail=True, methods=['post'])
    def toggle_follow(self, request, pk=None):
        return toggle_follow_request(view=self, request=request)
        
    @action(detail=True, methods=['put'])
    def timeblock(self, request, pk=None):
        return super().partial_update(request=request)
    
    def get_serializer_class(self): # TODO: refactor
            return self.serializer_classes[self.action] if self.action in self.serializer_classes else self.serializer_classes['default']
        