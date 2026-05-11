from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.common.viewsets import BaseViewSet, TenantQuerysetMixin
from services.photobooth.models.voucher import Voucher
from services.photobooth.rest.voucher.serializers import VoucherSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("VoucherViewSet",)


class VoucherViewSet(TenantQuerysetMixin, BaseViewSet):
    """
    ViewSet for managing Photobooth Vouchers.
    """

    queryset = Voucher.objects.select_related("tenant")
    serializer_class = VoucherSerializer
    lookup_field = "subid"
    search_fields = ["code"]
    my_tags = ["Photobooth Vouchers"]

    def perform_create(self, serializer):
        """
        Assign voucher owner automatically.
        """
        serializer.save(user=self.request.user, tenant=self.request.tenant)

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
            voucher = Voucher.objects.select_related("tenant").get(
                code=code,
                tenant=request.tenant,
                is_used=False,
            )
        except Voucher.DoesNotExist:
            return Response(
                {"detail": _("Invalid voucher code.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "voucher": {
                    "code": voucher.code,
                    "subid": voucher.subid,
                },
            },
            status=status.HTTP_200_OK,
        )
