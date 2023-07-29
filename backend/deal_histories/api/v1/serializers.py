"""Serializers of the 'Api' application v1."""

from rest_framework import serializers

from deals.models import File


class FileSerializer(serializers.ModelSerializer):
    """Serializer for file processing."""

    class Meta:
        fields = ("id", "file")
        model = File
