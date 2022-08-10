from rest_framework import viewsets

from . import models, serializers
from users.verify import JWTAuthentication


class PageViewSet(viewsets.ModelViewSet):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    
    def perform_create(self, serializer):
        auth = JWTAuthentication()
        user =  auth.authenticate(request=self.request)[0]
        serializer.save(owner=user)
        


class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
