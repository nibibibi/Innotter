from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from pages.models import Post

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    text = serializers.CharField()
    
    def create(self, validated_data):
        """
        Create and return new Post, given the validated data.
        """
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing Post, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance