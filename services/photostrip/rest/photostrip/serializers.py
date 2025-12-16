from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from services.file.models.file import File
from services.file.rest.file.serializers import FileSerializer
from services.gallery.models.gallery import Gallery
from services.photostrip.models.photostrip import Photostrip

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("PhotostripSerializer",)


class PhotostripSerializer(BaseModelSerializer):
    file = FileSerializer(read_only=True)

    # Write-only fields for creating the File model
    encrypted_file = serializers.FileField(write_only=True)
    encryption_iv = serializers.CharField(write_only=True)
    encrypted_key = serializers.CharField(write_only=True)
    mime_type = serializers.CharField(write_only=True)

    class Meta:
        model = Photostrip
        fields = [
            "pk",
            "file",
            "encrypted_file",
            "encryption_iv",
            "encrypted_key",
            "mime_type",
            "created",
            "updated",
        ]

    def create(self, validated_data):
        # Extract file fields
        file_data = {
            "encrypted_file": validated_data.pop("encrypted_file"),
            "encryption_iv": validated_data.pop("encryption_iv"),
            "encrypted_key": validated_data.pop("encrypted_key"),
            "mime_type": validated_data.pop("mime_type"),
        }

        # Create File instance
        file_obj = File.objects.create(**file_data)

        # Then create Gallery linked to file
        gallery = Photostrip.objects.create(
            file=file_obj,
            **validated_data,
        )

        return gallery
