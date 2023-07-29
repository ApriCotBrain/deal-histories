from rest_framework import serializers
from django.core.validators import FileExtensionValidator

from gems.models import File


class FileSerializer(serializers.ModelSerializer):
    # file = serializers.FileField(validators=(FileExtensionValidator(["csv"]),))

    class Meta:
        fields = ("id", "file")
        model = File
