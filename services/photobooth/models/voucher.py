from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model
from services.account.models import User

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "VoucherQuerySet",
    "VoucherManager",
    "Voucher",
)


class VoucherQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_VoucherManagerBase = models.Manager.from_queryset(VoucherQuerySet)  # type: type[VoucherQuerySet]


class VoucherManager(_VoucherManagerBase):
    pass


class Voucher(get_subid_model()):
    """
    Custom Voucher model to group permissions.
    """

    tenant = models.ForeignKey("tenant.Tenant", on_delete=models.CASCADE)
    code = models.CharField(_("code"), max_length=255)

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = VoucherManager()

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")

    def __str__(self) -> str:
        return f"Photobooth Voucher {self.code}"
