from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from services.photobooth.models import File, Event, Session

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

    class Meta:
        model = File
        fields = [
            "pk",
            "event",
            "session",
            "file",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")
