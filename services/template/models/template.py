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
    "TemplateQuerySet",
    "TemplateManager",
    "Template",
)


class TemplateQuerySet(models.QuerySet):
    def active(self) -> models.QuerySet:
        return self.filter(is_active=True)


_TemplateManagerBase = models.Manager.from_queryset(TemplateQuerySet)


class TemplateManager(_TemplateManagerBase):
    pass


class Template(get_subid_model()):
    """
    Photostrip template base model.
    """

    type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    location = models.FileField(upload_to="templates")

    is_active = models.BooleanField(default=True)

    objects = TemplateManager()

    class Meta:
        verbose_name = _("template")
        verbose_name_plural = _("templates")

    def __str__(self) -> str:
        return f"{self.name} ({self.pk})"
