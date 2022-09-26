from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "image_s3_path",
            "title",
            "role",
            "is_blocked",
            "favourite_posts",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Just a registration serializer for API testing
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.Roles, default=User.Roles.USER)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "role",
        ]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
