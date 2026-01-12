from __future__ import annotations

from services.transaction.rest.topup.serializers import BaseTopupTransactionSerializer

from services.transaction.rest.topup.serializers import TopupTransactionSerializer
from services.activity.rest.activity.serializers import ActivitySerializer
from services.activity.models.activity import Activity

from django.db.models.aggregates import Sum

import logging
from typing import TYPE_CHECKING

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from services.account.models import User
from services.transaction.models import TopupTransaction
from services.photostrip.models import Photostrip

if TYPE_CHECKING:
    from rest_framework.request import Request

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

logger = logging.getLogger(__name__)

__all__ = (
    "DashboardStatsViewSet",
)


class DashboardStatsViewSet(ViewSet):
    """
    ViewSet to return dashboard statistics with separate endpoints.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def users(self, request: Request) -> Response:
        count = User.objects.count()
        return Response({"count": count})

    @action(detail=False, methods=["get"])
    def topups(self, request: Request) -> Response:
        count = TopupTransaction.objects.filter(
            status=TopupTransaction.Status.SUCCESS
        ).count()
        return Response({"count": count})

    @action(detail=False, methods=["get"])
    def photostrips(self, request: Request) -> Response:
        count = Photostrip.objects.count()
        return Response({"count": count})

    @action(detail=False, methods=["get"])
    def revenues(self, request: Request) -> Response:
        transactions = TopupTransaction.objects.filter(
            status=TopupTransaction.Status.SUCCESS
        ).aggregate(Sum("total"))
        return Response({"count": transactions["total__sum"]})

    @action(detail=False, methods=["get"])
    def activities(self, request: Request) -> Response:
        last_activities = Activity.objects.all().order_by("-created")[:10]
        serializer = ActivitySerializer(last_activities, many=True)
        return Response({"activities": serializer.data})


    @action(detail=False, methods=["get"])
    def transactions(self, request: Request) -> Response:
        last_transactions = TopupTransaction.objects.filter(
            status=TopupTransaction.Status.SUCCESS
        ).order_by("-created")[:10]
        serializer = BaseTopupTransactionSerializer(last_transactions, many=True)
        return Response({"transactions": serializer.data})
