from __future__ import annotations

import logging

from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from services.subscription.models import Subscription
from services.subscription.rest.plan.serializers import (
    SubscriptionPlanSerializerSimple,
)
from services.subscription.models import SubscriptionPlan
from services.tenant.models import Tenant
from services.tenant.rest.tenant.serializers import TenantSerializerSimple

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionSerializer",
    "SubscriptionSerializerSimple",
)


class SubscriptionSerializer(BaseModelSerializer):
    tenant = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Tenant.objects.all(),
        required=True,
    )
    plan = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=SubscriptionPlan.objects.all(),
        required=True,
    )
    is_active = serializers.SerializerMethodField()
    is_trial = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "pk",
            "tenant",
            "plan",
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['plan'] = SubscriptionPlanSerializerSimple(instance.plan).data
        representation['tenant'] = TenantSerializerSimple(instance.tenant).data
        return representation

    def get_is_active(self, obj):
        return obj.is_active

    def get_is_trial(self, obj):
        return obj.is_trial


class SubscriptionSerializerSimple(BaseModelSerializer):
    plan = SubscriptionPlanSerializerSimple(read_only=True)
    # tenant = TenantSerializerSimple(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "pk",
            "plan",
            # "tenant",
            "status",
            "current_period_start",
            "current_period_end",
        ]