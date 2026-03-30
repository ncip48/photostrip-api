from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from core.mixin import FloatToIntRepresentationMixin
from services.photobooth.models import Event

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("EventSerializer",)


class EventSerializer(FloatToIntRepresentationMixin, BaseModelSerializer):
    """
    Serializer for Photobooth Event
    """

    float_to_int_fields = (
        "iso",
        "price",
        "max_print_strip",
        "additional_price_per_print_strip",
        "time_payment",
        "time_take_picture",
        "time_configure_photostrip",
        "time_download",
    )

    class Meta:
        model = Event
        fields = [
            "pk",
            "title",
            "subtitle",
            "background",
            # Pricing
            "is_paid_event",
            "price",
            "max_print_strip",
            "additional_price_per_print_strip",
            # Camera settings
            "countdown_timer",
            "orientation",
            # Time settings (ms)
            "time_payment",
            "time_take_picture",
            "time_configure_photostrip",
            "time_download",
            # Meta
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")
