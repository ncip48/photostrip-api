from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from services.photobooth.models import Voucher

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("VoucherSerializer",)


class VoucherSerializer(BaseModelSerializer):
    """
    Serializer for Photobooth Voucher
    """

    class Meta:
        model = Voucher
        fields = [
            "pk",
            "subid",
            "event",
            "code",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")
