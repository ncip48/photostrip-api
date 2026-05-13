from __future__ import annotations

import logging

from rest_framework.decorators import action
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet
from services.subscription.models import SubscriptionPlan
from services.subscription.rest.plan.serializers import (
    SubscriptionPlanSerializer,
)

logger = logging.getLogger(__name__)

__all__ = ("SubscriptionPlanViewSet",)


class SubscriptionPlanViewSet(BaseViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field = "subid"
    search_fields = ["name", "code", "description"]
    # required_perms = [
    #     "account.add_role",
    #     "account.change_role",
    #     "account.delete_role",
    #     "account.view_role",
    # ]
    ordering = ["price", "id"]
    my_tags = ["Subscription Plans"]

    @action(detail=False, methods=["get"], url_path="active")
    def active(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset().active())
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)