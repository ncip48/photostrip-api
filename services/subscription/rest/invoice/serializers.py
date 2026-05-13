from __future__ import annotations

import logging

from core.common.serializers import BaseModelSerializer
from services.subscription.models import SubscriptionInvoice

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionInvoiceSerializer",
    "SubscriptionInvoiceSerializerSimple",
)


class SubscriptionInvoiceSerializer(BaseModelSerializer):
    class Meta:
        model = SubscriptionInvoice
        fields = [
            "pk",
            "tenant",
            "subscription",
            "invoice_number",
            "amount",
            "currency",
            "status",
            "payment_method",
            "payment_reference",
            "issued_at",
            "due_at",
            "paid_at",
            "notes",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")


class SubscriptionInvoiceSerializerSimple(BaseModelSerializer):
    class Meta:
        model = SubscriptionInvoice
        fields = [
            "pk",
            "invoice_number",
            "amount",
            "currency",
            "status",
            "issued_at",
            "due_at",
            "paid_at",
        ]