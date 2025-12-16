from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _

from core.common.viewsets import BaseViewSet
from services.product.models.product import Product
from services.product.rest.product.serializers import ProductSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("ProductViewSet",)


class ProductViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "subid"
    search_fields = []
    my_tags = ["Products"]

    ordering = ["id"]
