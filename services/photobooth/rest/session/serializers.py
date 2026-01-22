from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rest_framework import serializers
from core.common.serializers import BaseModelSerializer
from services.photobooth.models import Session, Event, Voucher

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("SessionSerializer",)


class SessionSerializer(BaseModelSerializer):
    """
    Serializer for Photobooth Session
    """
    event = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Event.objects.all(),
        required=True,
    )
    voucher = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Voucher.objects.all(),
        required=False,
    )

    class Meta:
        model = Session
        fields = [
            "pk",
            "event",
            "voucher",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")
