from dataclasses import field
from rest_framework import serializers

from ..models import Page


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class TimeBlockPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['unblock_date']
