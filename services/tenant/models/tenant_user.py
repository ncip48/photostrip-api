from __future__ import annotations
from django.db import models
from core.common.models import get_subid_model
from typing import TYPE_CHECKING
import logging
from django.utils.translation import gettext_lazy as _
from .tenant import Tenant
from services.account.models import User
from django.utils import timezone

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)
__all__ = (
    "TenantUserQuerySet",
    "TenantUserManager",
    "TenantUser",
)


class TenantUserQuerySet(models.QuerySet):
    pass


_TenantUserManagerBase = models.Manager.from_queryset(TenantUserQuerySet)  # type: type[TenantUserQuerySet]


class TenantUserManager(_TenantUserManagerBase):
    pass


class TenantUser(get_subid_model()):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_owner = models.BooleanField(_("owner status"), default=False)
    is_active = models.BooleanField(_("active status"), default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = TenantUserManager()

    class Meta:
        unique_together = (("tenant", "user"),)

    def update_active_status(self, value: bool, *, save: bool = True):
        self.is_active = value
        if save:
            self.save(update_fields=["is_active"])

    def activate(self, *, save: bool = True):
        self.update_active_status(True, save=save)

    def deactivate(self, *, save: bool = True):
        self.update_active_status(False, save=save)
