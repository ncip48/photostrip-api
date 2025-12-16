from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model
from services.template.models.template import Template

if TYPE_CHECKING:
    from services.account.models import User

logger = logging.getLogger(__name__)

__all__ = (
    "DropzoneQuerySet",
    "DropzoneManager",
    "Dropzone",
)


class DropzoneQuerySet(models.QuerySet):
    def active(self) -> models.QuerySet:
        return self.filter(is_active=True)


_DropzoneManagerBase = models.Manager.from_queryset(DropzoneQuerySet)


class DropzoneManager(_DropzoneManagerBase):
    pass


class Dropzone(get_subid_model()):
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, related_name="dropzones"
    )
    top = models.PositiveIntegerField()
    left = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()

    objects = DropzoneManager()

    class Meta:
        verbose_name = _("dropzone")
        verbose_name_plural = _("dropzones")

    def __str__(self) -> str:
        return f"{self.dropzone_id} @ {self.template.template_id}"
