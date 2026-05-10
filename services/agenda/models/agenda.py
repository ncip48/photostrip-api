from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model
from services.account.models import User
from services.tenant.models import Tenant

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "AgendaQuerySet",
    "AgendaManager",
    "Agenda",
)


class AgendaQuerySet(models.QuerySet):
    def owned(self, user: User, tenant: Tenant) -> models.QuerySet:
        return self.filter(tenant=tenant)

    def active(self) -> models.QuerySet:
        return self.exclude(status=Agenda.BookingStatus.CANCELLED)

    def between(self, start_at, end_at) -> models.QuerySet:
        """
        Return bookings that overlap with a given date range.
        """
        return self.filter(
            start_at__lt=end_at,
            end_at__gt=start_at,
        )

    def for_calendar(self) -> models.QuerySet:
        return self.select_related("tenant", "event", "created_by")


_AgendaManagerBase = models.Manager.from_queryset(AgendaQuerySet)


class AgendaManager(_AgendaManagerBase):
    pass


class Agenda(get_subid_model()):
    """
    Manual calendar booking for photobooth events.

    Example use case:
    Admin manually inputs a customer booking into calendar:
    - wedding event
    - birthday event
    - corporate event
    - graduation event
    - booth rental schedule
    """

    class BookingStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PENDING = "pending", _("Pending")
        CONFIRMED = "confirmed", _("Confirmed")
        COMPLETED = "completed", _("Completed")
        CANCELLED = "cancelled", _("Cancelled")

    class BookingSource(models.TextChoices):
        MANUAL = "manual", _("Manual Input")
        WEBSITE = "website", _("Website")
        WHATSAPP = "whatsapp", _("WhatsApp")
        OTHER = "other", _("Other")

    tenant = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE,
        related_name="photobooth_event_agendas",
    )

    event = models.ForeignKey(
        "photobooth.Event",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agendas",
        help_text=_("Optional existing photobooth event/package."),
    )

    created_by = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_photobooth_agendas",
    )

    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)

    customer_name = models.CharField(_("customer name"), max_length=255)
    customer_phone = models.CharField(_("customer phone"), max_length=50, blank=True)
    customer_email = models.EmailField(_("customer email"), blank=True)

    location = models.TextField(_("location"), blank=True)

    start_at = models.DateTimeField(_("start at"))
    end_at = models.DateTimeField(_("end at"))

    status = models.CharField(
        _("status"),
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.CONFIRMED,
    )

    source = models.CharField(
        _("source"),
        max_length=20,
        choices=BookingSource.choices,
        default=BookingSource.MANUAL,
    )

    all_day = models.BooleanField(_("all day"), default=False)

    color = models.CharField(
        _("calendar color"),
        max_length=20,
        blank=True,
        help_text=_("Optional frontend calendar color, example: #3788d8"),
    )

    notes = models.TextField(_("internal notes"), blank=True)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = AgendaManager()

    class Meta:
        verbose_name = _("Agenda")
        verbose_name_plural = _("Agendas")
        ordering = ["start_at", "-id"]
        indexes = [
            models.Index(fields=["tenant", "start_at"]),
            models.Index(fields=["tenant", "end_at"]),
            models.Index(fields=["tenant", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} - {self.customer_name}"

    @property
    def duration_minutes(self) -> int:
        if not self.start_at or not self.end_at:
            return 0
        return int((self.end_at - self.start_at).total_seconds() / 60)

    def clean(self):
        super().clean()

        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValidationError(
                {
                    "end_at": _("End time must be greater than start time."),
                }
            )