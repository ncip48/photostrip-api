from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rest_framework import serializers
from core.common.serializers import BaseModelSerializer
from services.photobooth.models import Session, Event, Voucher
from services.photobooth.rest.event.serializers import EventSerializerSimple
from services.photobooth.rest.voucher.serializers import VoucherSerializerSimple

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["event"] = (
            EventSerializerSimple(instance.event).data if instance.event else None
        )

        representation["voucher"] = (
            VoucherSerializerSimple(instance.voucher).data if instance.voucher else None
        )

        return representation
