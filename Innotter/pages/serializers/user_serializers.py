from rest_framework import serializers
from users.models import User


class UserFavouritePostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['favourite_posts']
        