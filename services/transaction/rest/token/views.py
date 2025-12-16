from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet
from services.transaction.models.token import TokenTransaction
from services.transaction.rest.token.serializers import TokenTransactionSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TokenTransactionViewSet",)


class TokenTransactionViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = TokenTransaction.objects.all()
    serializer_class = TokenTransactionSerializer
    lookup_field = "subid"
    search_fields = []
    my_tags = ["Tokens"]

    def get_queryset(self):
        return self.queryset.owned(user=self.request.user)

    def summary(self, request):
        total_topup = TokenTransaction.objects.topup_amount(user=self.request.user)
        total_used = TokenTransaction.objects.spent_amount(user=self.request.user)
        return Response({"total_topup": total_topup, "total_used": total_used})
