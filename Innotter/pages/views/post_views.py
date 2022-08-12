from ..permissons import IsAuthorOrReadOnly, IsAlreadyWelcomed
from ..models import Post
from ..serializers.post_serializers import PostSerializer
from rest_framework import viewsets


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly, IsAlreadyWelcomed]
    queryset = Post.objects.all()
    serializer_class = PostSerializer