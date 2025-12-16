from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common.viewsets import BaseViewSet
from services.transaction.models.token import TokenTransaction
from services.transaction.models.topup import TopupTransaction
from services.transaction.rest.topup.serializers import TopupTransactionSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TopupTransactionViewSet",)


class TopupTransactionViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = TopupTransaction.objects.all()
    serializer_class = TopupTransactionSerializer
    lookup_field = "subid"
    search_fields = []
    my_tags = ["Topups"]

    def get_queryset(self):
        return self.queryset.owned(user=self.request.user)


class TopupWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.data
        # process webhook
        status = payload.get("status")
        order_id = payload.get("order_id")
        if status == "completed":
            topup = TopupTransaction.objects.filter(reference=order_id).first()

            # If not found → ignore
            if not topup:
                return Response({"message": "topup not found"}, status=404)

            # If already processed → don't do anything
            if topup.status == TopupTransaction.Status.SUCCESS:
                return Response({"message": "already processed"}, status=200)

            # Process successful topup
            topup.status = TopupTransaction.Status.SUCCESS
            topup.save()

            TokenTransaction.objects.create(
                user=topup.user,
                type=TokenTransaction.Choices.TOPUP,
                amount=topup.token,
                method="QRIS",
                note=f"Topup #{topup.reference}",
            )

        elif status == "failed":
            TopupTransaction.objects.filter(reference=order_id).update(
                status=TopupTransaction.Status.FAILED
            )
        return Response(payload, status=200)
