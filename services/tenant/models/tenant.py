from __future__ import annotations
from django.db import models
from core.common.models import get_subid_model
from typing import TYPE_CHECKING, Self
import logging
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)
__all__ = (
    "TenantQuerySet",
    "TenantManager",
    "Tenant",
)


class TenantQuerySet(models.QuerySet):
    def accessible_by_user(self, user_id: int) -> Self:
        return self.filter(
            tenantuser__user_id=user_id,
            tenantuser__is_registered=True,
            tenantuser__is_active=True,
        )


_TenantManagerBase = models.Manager.from_queryset(TenantQuerySet)  # type: type[TenantQuerySet]


class TenantManager(_TenantManagerBase):
    pass


class Tenant(get_subid_model()):
    name = models.CharField(max_length=255)
    photo = models.ImageField(
        upload_to="tenants", max_length=100, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = TenantManager()

    def set_active(self):
        """Set the tenant as active and save."""
        self.is_active = True
        self.save(update_fields=["is_active", "updated"])

    def set_inactive(self):
        """Set the tenant as inactive and save."""
        self.is_active = False
        self.save(update_fields=["is_active", "updated"])

    def __str__(self):
        return f"{self.name} ({self.is_active})"
