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
    "EventQuerySet",
    "EventManager",
    "Event",
)


class EventQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_EventManagerBase = models.Manager.from_queryset(EventQuerySet)  # type: type[EventQuerySet]


class EventManager(_EventManagerBase):
    pass


class Event(get_subid_model()):
    """
    Custom Event model to group permissions.
    """

    title = models.CharField(_("title"), max_length=255)
    subtitle = models.CharField(_("subtitle"), max_length=255)
    background = models.ImageField(
        _("background"), upload_to="photobooth/event/background"
    )

    # Settings
    is_paid_event = models.BooleanField(_("paid event"), default=False)
    price = models.IntegerField(_("price"), default=0)
    max_print_strip = models.IntegerField(_("max print strip"), default=2)
    additional_price_per_print_strip = models.IntegerField(
        _("additional price per print strip"), null=True, blank=True
    )

    countdown_timer = models.IntegerField(_("countdown timer"), default=10)
    orientation = models.CharField(
        _("orientation"),
        max_length=10,
        choices=[
            ("portrait", "Portrait"),
            ("landscape", "Landscape"),
        ],
        default="landscape",
    )

    # Time in ms
    time_payment = models.PositiveIntegerField(_("time payment"), default=60)
    time_take_picture = models.PositiveIntegerField(_("time take picture"), default=180)
    time_configure_photostrip = models.PositiveIntegerField(
        _("time configure photostrip"), default=120
    )
    time_download = models.PositiveIntegerField(_("time download"), default=60)

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = EventManager()

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __str__(self) -> str:
        return f"Photobooth Event {self.title}"
