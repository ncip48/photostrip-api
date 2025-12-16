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
    "TemplateSizeQuerySet",
    "TemplateSizeManager",
    "TemplateSize",
)


class TemplateSizeQuerySet(models.QuerySet):
    pass


_TemplateSizeManagerBase = models.Manager.from_queryset(TemplateSizeQuerySet)


class TemplateSizeManager(_TemplateSizeManagerBase):
    pass


class TemplateSize(get_subid_model()):
    template = models.OneToOneField(
        Template, on_delete=models.CASCADE, related_name="size"
    )
    width_photostrip = models.PositiveIntegerField()
    height_photostrip = models.PositiveIntegerField()

    objects = TemplateSizeManager()

    class Meta:
        verbose_name = _("template size")
        verbose_name_plural = _("template sizes")

    def __str__(self) -> str:
        return f"Size of {self.template.template_id}"
