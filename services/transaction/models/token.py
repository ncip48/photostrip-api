from __future__ import annotations

import logging
from decimal import Decimal
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import DecimalField, Sum, Value
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from core.common.models import get_subid_model

if TYPE_CHECKING:
    from services.account.models import User

logger = logging.getLogger(__name__)

__all__ = (
    "TokenTransactionQuerySet",
    "TokenTransactionManager",
    "TokenTransaction",
)


class TokenTransactionQuerySet(models.QuerySet):
    ZERO = Value(Decimal("0"), output_field=DecimalField())

    def owned(self, user):
        return self.filter(user=user)

    def spent_amount(self, user):
        return self.filter(type="spend", user=user).aggregate(
            total=Coalesce(Sum("amount"), self.ZERO)
        )["total"]

    def topup_amount(self, user):
        return self.filter(type="topup", user=user).aggregate(
            total=Coalesce(Sum("amount"), self.ZERO)
        )["total"]

    def gift_amount(self, user):
        return self.filter(type="gift", user=user).aggregate(
            total=Coalesce(Sum("amount"), self.ZERO)
        )["total"]

    def current_token(self, user):
        topup = self.topup_amount(user)
        gift = self.gift_amount(user)
        spend = self.spent_amount(user)
        return (topup + gift) - spend


_TokenTransactionManagerBase = models.Manager.from_queryset(TokenTransactionQuerySet)


class TokenTransactionManager(_TokenTransactionManagerBase):
    def get_queryset(self):
        return TokenTransactionQuerySet(self.model, using=self._db)

    def current_token(self, user):
        return self.get_queryset().current_token(user)

    def spent_amount(self, user):
        return self.get_queryset().spent_amount(user)

    def topup_amount(self, user):
        return self.get_queryset().topup_amount(user)

    def gift_amount(self, user):
        return self.get_queryset().gift_amount(user)

    def usage_rates(self, user):
        return self.get_queryset().spent_amount(user) / 7

    def token_usage_activity(self, user):
        today = timezone.localdate()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)          # Sunday

        queryset = (
            self.get_queryset()
            .filter(
                user=user,
                type__iexact="spend",
                created__date__range=(start_of_week, end_of_week),
            )
            .annotate(day=TruncDate("created"))
            .values("day")
            .annotate(tokens=Sum("amount"))
            .order_by("day")
        )

        # Prepare full week (Mon–Sun), default = 0
        chart_map = {
            (start_of_week + timedelta(days=i)): 0
            for i in range(7)
        }

        for row in queryset:
            chart_map[row["day"]] = row["tokens"]

        # Final format for Recharts
        chart_data = [
            {
                "day": (start_of_week + timedelta(days=i)).strftime("%a"),
                "tokens": chart_map[start_of_week + timedelta(days=i)],
            }
            for i in range(7)
        ]

        return chart_data


class TokenTransaction(get_subid_model()):
    class Choices(models.TextChoices):
        TOPUP = "topup", "Top Up"
        SPEND = "spend", "Spend"
        GIFT = "gift", "Gift"

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="tokens"
    )
    type = models.CharField(max_length=20, choices=Choices.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, null=True, blank=True)

    note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = TokenTransactionManager()

    class Meta:
        verbose_name = _("token transaction")
        verbose_name_plural = _("token transactions")

    def __str__(self) -> str:
        return f"{self.user} ({self.pk})"
