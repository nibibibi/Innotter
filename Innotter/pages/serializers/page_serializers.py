from rest_framework import serializers

from ..models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class TimeBlockPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["unblock_date"]


class EditPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["name", "uuid", "description"]


class ListRequestsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ["follow_requests"]


class ToggleFollowRequestPageSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Page
        fields = ["follow_requests", "followers"]


class ToggleTagPageSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(required=True)

    class Meta:
        model = Page
        fields = ["tags"]
