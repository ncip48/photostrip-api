from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from core.mixin import FloatToIntRepresentationMixin
from services.transaction.models.token import TokenTransaction

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TokenTransactionSerializer",)


class TokenTransactionSerializer(FloatToIntRepresentationMixin, BaseModelSerializer):
    float_to_int_fields = ("amount",)

    class Meta:
        model = TokenTransaction
        fields = [
            "pk",
            "type",
            "amount",
            "note",
            "method",
            "created",
        ]
