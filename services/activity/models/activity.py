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
    "ActivityQuerySet",
    "ActivityManager",
    "Activity",
)


class ActivityQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_ActivityManagerBase = models.Manager.from_queryset(ActivityQuerySet)  # type: type[ActivityQuerySet]


class ActivityManager(_ActivityManagerBase):
    pass


class Activity(get_subid_model()):
    """
    Custom Activity model to group permissions.
    """

    activity = models.CharField(max_length=255)
    reference = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = ActivityManager()

    class Meta:
        verbose_name = _("activity")
        verbose_name_plural = _("activities")

    def __str__(self) -> str:
        return f"Activity {self.id}"
