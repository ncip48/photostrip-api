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
    "SessionQuerySet",
    "SessionManager",
    "Session",
)


class SessionQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_SessionManagerBase = models.Manager.from_queryset(SessionQuerySet)  # type: type[SessionQuerySet]


class SessionManager(_SessionManagerBase):
    pass


class Session(get_subid_model()):
    """
    Custom Session model to group permissions.
    """
    event = models.ForeignKey("photobooth.Event", on_delete=models.CASCADE)
    voucher = models.ForeignKey("photobooth.Voucher", on_delete=models.CASCADE, null=True, blank=True)

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = SessionManager()

    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    def __str__(self) -> str:
        return f"Photobooth Session {self.id}"
