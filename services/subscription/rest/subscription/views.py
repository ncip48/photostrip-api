from __future__ import annotations

import logging

from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet, TenantQuerysetMixin
from services.subscription.models import Subscription
from services.subscription.rest.subscription.serializers import SubscriptionSerializer

logger = logging.getLogger(__name__)

__all__ = ("SubscriptionViewSet",)


class SubscriptionViewSet(BaseViewSet, TenantQuerysetMixin):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    lookup_field = "subid"
    search_fields = []
    ordering = ["-created"]
    my_tags = ["Subscriptions"]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("tenant", "plan")

        status_param = self.request.query_params.get("status")
        tenant = self.request.query_params.get("tenant")

        if status_param:
            qs = qs.filter(status=status_param)

        if tenant:
            qs = qs.filter(tenant_id=tenant)

        return qs

    @action(detail=False, methods=["get"], url_path="current")
    def current(self, request, *args, **kwargs):
        tenant = getattr(request, "tenant", None)

        if not tenant:
            return Response({"detail": "Tenant not found."}, status=400)

        subscription = (
            self.get_queryset()
            .filter(tenant=tenant)
            .order_by("-created")
            .first()
        )

        if not subscription:
            return Response({"detail": "Subscription not found."}, status=404)

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.status = Subscription.SubscriptionStatus.CANCELLED
        subscription.cancelled_at = timezone.now()
        subscription.cancel_at_period_end = False
        subscription.save(
            update_fields=[
                "status",
                "cancelled_at",
                "cancel_at_period_end",
                "updated",
            ]
        )

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="cancel-at-period-end")
    def cancel_at_period_end(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.cancel_at_period_end = True
        subscription.save(update_fields=["cancel_at_period_end", "updated"])

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="reactivate")
    def reactivate(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.status = Subscription.SubscriptionStatus.ACTIVE
        subscription.cancel_at_period_end = False
        subscription.cancelled_at = None
        subscription.save(
            update_fields=[
                "status",
                "cancel_at_period_end",
                "cancelled_at",
                "updated",
            ]
        )

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)