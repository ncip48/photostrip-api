from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from services.photobooth.rest.event.serializers import EventSerializerSimple
from services.photobooth.models import Voucher
from rest_framework import serializers


if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("VoucherSerializer",)


class VoucherSerializer(BaseModelSerializer):
    """
    Serializer for Photobooth Voucher
    """

    is_used = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = Voucher
        fields = [
            "pk",
            "is_used",
            "event",
            "code",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")

    def get_is_used(self, obj):
        return obj.session_set.exists()

    def get_event(self, obj):
        return (
            EventSerializerSimple(obj.session_set.last().event).data
            if obj.session_set.exists()
            else None
        )


class VoucherSerializerSimple(BaseModelSerializer):
    class Meta:
        model = Voucher
        fields = [
            "pk",
            "code",
        ]
