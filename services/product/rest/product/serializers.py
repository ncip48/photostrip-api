from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from core.mixin import FloatToIntRepresentationMixin
from services.product.models.product import Product
from services.transaction.models.topup import TopupTransaction

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("ProductSerializer",)


class ProductSerializer(FloatToIntRepresentationMixin, BaseModelSerializer):
    float_to_int_fields = ("price", "token")

    is_popular = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "pk",
            "token",
            "price",
            "is_active",
            "is_popular",
            "created",
        ]

    def get_is_popular(self, obj: Product) -> bool:
        most_popular = (
            TopupTransaction.objects.values("product")
            .filter(status=TopupTransaction.Status.SUCCESS)
            .annotate(total=models.Count("id"))
            .order_by("-total")
            .first()
        )

        if not most_popular:
            return False

        return most_popular["product"] == obj.pk
