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
    "GalleryQuerySet",
    "GalleryManager",
    "Gallery",
)


class GalleryQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_GalleryManagerBase = models.Manager.from_queryset(GalleryQuerySet)  # type: type[GalleryQuerySet]


class GalleryManager(_GalleryManagerBase):
    pass


class Gallery(get_subid_model()):
    """
    Custom Gallery model to group permissions.
    """

    file = models.ForeignKey("file.File", on_delete=models.CASCADE)

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = GalleryManager()

    class Meta:
        verbose_name = _("gallery")
        verbose_name_plural = _("galleries")

    def __str__(self) -> str:
        return f"Gallery {self.id}"
