from rest_framework import serializers

from ..models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class RetrievePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ["follow_requests"]


class RetrievePrivatePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        exclude = ["follow_requests", "followers", "description"]
