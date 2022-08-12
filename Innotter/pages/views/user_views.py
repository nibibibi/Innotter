from ..mixins.user_mixins import UserViewSetMixin
from rest_framework.decorators import action
from ..services import user_services


class UserViewSet(UserViewSetMixin):
    
    @action(detail=True, methods=['post',])
    def block(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action=self.action)
    
    @action(detail=True, methods=['post',])
    def unblock(self, request, pk=None):
        return user_services.toggle_is_blocked(user=self.get_object(), action=self.action)
