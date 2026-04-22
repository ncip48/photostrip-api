from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from core.mixin import FloatToIntRepresentationMixin
from services.photobooth.models import Event
from django.db import transaction

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
            "is_default",
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

    def create(self, validated_data):
        request = self.context["request"]
        tenant = getattr(request, "tenant", None)

        is_default = validated_data.get("is_default", False)

        with transaction.atomic():
            if tenant and is_default:
                Event.objects.filter(tenant=tenant, is_default=True).update(
                    is_default=False
                )

            validated_data["tenant"] = tenant
            validated_data["user"] = request.user

            return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context["request"]
        tenant = getattr(request, "tenant", None)

        is_default = validated_data.get("is_default", instance.is_default)

        with transaction.atomic():
            if tenant and is_default:
                Event.objects.filter(tenant=tenant, is_default=True).exclude(
                    pk=instance.pk
                ).update(is_default=False)

            return super().update(instance, validated_data)
