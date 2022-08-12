from ..permissons import IsWelcome, IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class PageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsWelcome, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def list(self, request):
        pass
    
    def retrieve(self, request, pk=None):
        pass
    
    @action(detail=True, methods=['post',])
    def block_until(self, request, pk=None):
        pass