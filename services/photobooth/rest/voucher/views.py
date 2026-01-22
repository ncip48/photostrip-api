from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.common.viewsets import BaseViewSet
from services.photobooth.models.voucher import Voucher
from services.photobooth.rest.voucher.serializers import VoucherSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("VoucherViewSet",)


class VoucherViewSet(BaseViewSet):
    """
    ViewSet for managing Photobooth Vouchers.
    """

    queryset = Voucher.objects.select_related("event")
    serializer_class = VoucherSerializer
    lookup_field = "subid"
    search_fields = ["code"]
    my_tags = ["Photobooth Vouchers"]

    def get_queryset(self):
        """
        Only vouchers owned by current user.
        """
        return self.queryset.owned(user=self.request.user)

    def perform_create(self, serializer):
        """
        Assign voucher owner automatically.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def validate(self, request):
        """
        Validate voucher code.
        """
        code = request.data.get("code")

        if not code:
            return Response(
                {"detail": _("Voucher code is required.")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            voucher = Voucher.objects.select_related("event").get(
                code=code,
            )
        except Voucher.DoesNotExist:
            return Response(
                {"valid": False, "detail": _("Invalid voucher code.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        event = voucher.event

        return Response(
            {
                "valid": True,
                "voucher": {
                    "code": voucher.code,
                    "subid": voucher.subid,
                },
                "event": {
                    "subid": event.subid,
                    "title": event.title,
                    "is_paid_event": event.is_paid_event,
                    "price": event.price,
                },
            },
            status=status.HTTP_200_OK,
        )
