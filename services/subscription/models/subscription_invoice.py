from __future__ import annotations

import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

logger = logging.getLogger(__name__)

__all__ = (
    "SubscriptionInvoiceQuerySet",
    "SubscriptionInvoiceManager",
    "SubscriptionInvoice",
)


class SubscriptionInvoiceQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status=SubscriptionInvoice.InvoiceStatus.PAID)

    def unpaid(self):
        return self.exclude(status=SubscriptionInvoice.InvoiceStatus.PAID)


_SubscriptionInvoiceManagerBase = models.Manager.from_queryset(SubscriptionInvoiceQuerySet)


class SubscriptionInvoiceManager(_SubscriptionInvoiceManagerBase):
    pass


class SubscriptionInvoice(get_subid_model()):
    """
    Invoice for tenant subscription payment.
    """

    class InvoiceStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        UNPAID = "unpaid", _("Unpaid")
        PAID = "paid", _("Paid")
        FAILED = "failed", _("Failed")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")

    class PaymentMethod(models.TextChoices):
        CASH = "cash", _("Cash")
        BANK_TRANSFER = "bank_transfer", _("Bank Transfer")
        QRIS = "qris", _("QRIS")
        EWALLET = "ewallet", _("E-Wallet")
        CARD = "card", _("Card")
        MANUAL = "manual", _("Manual")

    tenant = models.ForeignKey(
        "tenant.Tenant",
        on_delete=models.CASCADE,
        related_name="subscription_invoices",
    )

    subscription = models.ForeignKey(
        "subscription.Subscription",
        on_delete=models.CASCADE,
        related_name="invoices",
    )

    invoice_number = models.CharField(_("invoice number"), max_length=100, unique=True)

    amount = models.DecimalField(_("amount"), max_digits=12, decimal_places=2)
    currency = models.CharField(_("currency"), max_length=10, default="IDR")

    status = models.CharField(
        _("status"),
        max_length=20,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.UNPAID,
    )

    payment_method = models.CharField(
        _("payment method"),
        max_length=30,
        choices=PaymentMethod.choices,
        blank=True,
    )

    payment_reference = models.CharField(_("payment reference"), max_length=255, blank=True)

    issued_at = models.DateTimeField(_("issued at"))
    due_at = models.DateTimeField(_("due at"), null=True, blank=True)
    paid_at = models.DateTimeField(_("paid at"), null=True, blank=True)

    notes = models.TextField(_("notes"), blank=True)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = SubscriptionInvoiceManager()

    class Meta:
        verbose_name = _("Subscription Invoice")
        verbose_name_plural = _("Subscription Invoices")
        ordering = ["-issued_at"]
        indexes = [
            models.Index(fields=["tenant", "status"]),
            models.Index(fields=["invoice_number"]),
        ]

    def __str__(self) -> str:
        return self.invoice_number