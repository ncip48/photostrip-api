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
    "PhotostripQuerySet",
    "PhotostripManager",
    "Photostrip",
)


class PhotostripQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_PhotostripManagerBase = models.Manager.from_queryset(PhotostripQuerySet)  # type: type[PhotostripQuerySet]


class PhotostripManager(_PhotostripManagerBase):
    pass


class Photostrip(get_subid_model()):
    """
    Custom Photostrip model to group permissions.
    """

    file = models.ForeignKey("file.File", on_delete=models.CASCADE)

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = PhotostripManager()

    class Meta:
        verbose_name = _("photostrip")
        verbose_name_plural = _("photostrips")

    def __str__(self) -> str:
        return f"Photostrip {self.subid}"
