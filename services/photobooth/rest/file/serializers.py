from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rest_framework import serializers
from core.common.serializers import BaseModelSerializer
from services.photobooth.models import File, Event, Session
import boto3
from django.conf import settings

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
    file = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            "pk",
            "event",
            "session",
            # "file",
            "file",
            "live_video",
            "type",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")

    def get_file(self, obj):
        client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        return client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                "Key": obj.file.name,
            },
            ExpiresIn=3600,
        )
