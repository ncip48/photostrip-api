from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rest_framework import serializers
from core.common.serializers import BaseModelSerializer
from services.photobooth.models import File, Event, Session
# from core.common.s3 import generate_presigned_url

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("FileSerializer",)


class FileSerializer(BaseModelSerializer):
    """
    Serializer for Photobooth File
    """

    event = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Event.objects.all(),
        required=True,
    )
    session = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Session.objects.all(),
        required=True,
    )
    # file_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            "pk",
            "event",
            "session",
            "file",
            "thumbnail",
            # "file_url",
            "live_video",
            "type",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")

    # def get_file_url(self, obj):
    #     if not obj.file:
    #         return None

    #     if not obj.file.name:
    #         return None

    #     return generate_presigned_url(obj.file.name)
