from __future__ import annotations

import logging

from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from services.subscription.models import Subscription
from services.subscription.rest.subscription_plan.serializers import (
    SubscriptionPlanSerializerSimple,
)

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionSerializer",
    "SubscriptionSerializerSimple",
)


class SubscriptionSerializer(BaseModelSerializer):
    plan_detail = serializers.SerializerMethodField()
    is_active = serializers.SerializerMethodField()
    is_trial = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "pk",
            "subid",
            "tenant",
            "plan",
            "plan_detail",
            "status",
            "current_period_start",
            "current_period_end",
            "trial_start",
            "trial_end",
            "cancel_at_period_end",
            "cancelled_at",
            "is_active",
            "is_trial",
            "created",
            "updated",
        ]
        read_only_fields = (
            "created",
            "updated",
            "is_active",
            "is_trial",
            "plan_detail",
        )

    def get_plan_detail(self, obj):
        return SubscriptionPlanSerializerSimple(obj.plan).data

    def get_is_active(self, obj):
        return obj.is_active

    def get_is_trial(self, obj):
        return obj.is_trial


class SubscriptionSerializerSimple(BaseModelSerializer):
    plan = SubscriptionPlanSerializerSimple(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "pk",
            "subid",
            "plan",
            "status",
            "current_period_start",
            "current_period_end",
        ]