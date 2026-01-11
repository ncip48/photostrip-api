from __future__ import annotations

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
