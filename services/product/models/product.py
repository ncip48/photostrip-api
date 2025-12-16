from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

if TYPE_CHECKING:
    from services.account.models import User

logger = logging.getLogger(__name__)

__all__ = (
    "ProductQuerySet",
    "ProductManager",
    "Product",
)


class ProductQuerySet(models.QuerySet):
    pass


_ProductManagerBase = models.Manager.from_queryset(ProductQuerySet)


class ProductManager(_ProductManagerBase):
    pass


class Product(get_subid_model()):
    token = models.DecimalField(max_digits=12, decimal_places=2)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")

    def __str__(self) -> str:
        return f"{self.subid}: {self.token} {self.price}"
