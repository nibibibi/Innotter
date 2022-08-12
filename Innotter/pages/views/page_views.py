from rest_framework.decorators import action
from ..services.page_services import toggle_follow_or_request_invitation
from ..mixins.page_mixins import PageViewSetMixin

class PageViewSet(PageViewSetMixin):

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    @action(detail=True, methods=['post','get'])
    def follow(self, request, pk=None):
        return toggle_follow_or_request_invitation(view=self, request=request)
    
    @action(detail=True, methods=['post','get'])
    def unfollow(self, request, pk=None):
        return toggle_follow_or_request_invitation(view=self, request=request)
        