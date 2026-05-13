from __future__ import annotations

import logging

from core.common.serializers import BaseModelSerializer
from services.subscription.models import SubscriptionPlan
from core.mixin import FloatToIntRepresentationMixin

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionPlanSerializer",
    "SubscriptionPlanSerializerSimple",
)


class SubscriptionPlanSerializer(FloatToIntRepresentationMixin, BaseModelSerializer):
    float_to_int_fields = ["price"]
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            "pk",
            "name",
            "code",
            "description",
            "price",
            "currency",
            "billing_interval",
            # "max_users",
            # "max_events_per_month",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")


class SubscriptionPlanSerializerSimple(FloatToIntRepresentationMixin, BaseModelSerializer):
    float_to_int_fields = ["price"]
    
    class Meta:
        model = SubscriptionPlan
        fields = [
            "pk",
            "name",
            "code",
            "price",
            "currency",
            "billing_interval",
        ]