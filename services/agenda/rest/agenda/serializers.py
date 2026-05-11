from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.common.serializers import BaseModelSerializer
from services.agenda.models import Agenda
from services.photobooth.rest.event.serializers import EventSerializerSimple
from services.account.rest.user.serializers import UserSerializerSimple

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "AgendaSerializer",
    "AgendaSerializerSimple",
    "AgendaCalendarSerializer",
    "AgendaTableSerializer",
)


class AgendaSerializer(BaseModelSerializer):
    """
    Full serializer for creating, updating, and deleting photobooth calendar bookings.
    Used by admin/manual input.
    """

    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        fields = [
            "pk",
            # "tenant",
            "event",
            "created_by",
            "title",
            "description",
            "customer_name",
            "customer_phone",
            "customer_email",
            "location",
            "start_at",
            "end_at",
            "duration_minutes",
            "status",
            "source",
            "all_day",
            "color",
            "notes",
            "created",
            "updated",
        ]
        read_only_fields = (
            "created",
            "tenant",
            "updated",
            "created_by",
            "duration_minutes",
            "event_detail",
        )
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["event"] = (
            EventSerializerSimple(instance.event).data if instance.event else None
        )
        
        representation["created_by"] = (
            UserSerializerSimple(instance.created_by).data if instance.created_by else None
        )

        return representation

    def get_event_detail(self, obj):
        return EventSerializerSimple(obj.event).data if obj.event else None

    def get_duration_minutes(self, obj):
        return obj.duration_minutes

    def validate(self, attrs):
        start_at = attrs.get("start_at", getattr(self.instance, "start_at", None))
        end_at = attrs.get("end_at", getattr(self.instance, "end_at", None))
        tenant = attrs.get("tenant", getattr(self.instance, "tenant", None))
        status = attrs.get("status", getattr(self.instance, "status", None))

        if start_at and end_at and end_at <= start_at:
            raise serializers.ValidationError(
                {
                    "end_at": _("End time must be greater than start time."),
                }
            )

        # Optional overlap validation.
        # Cancelled bookings are ignored.
        # Remove this block if overlapping bookings should be allowed.
        # if tenant and start_at and end_at and status != Agenda.BookingStatus.CANCELLED:
        #     qs = Agenda.objects.filter(
        #         tenant=tenant,
        #         start_at__lt=end_at,
        #         end_at__gt=start_at,
        #     ).exclude(status=Agenda.BookingStatus.CANCELLED)

        #     if self.instance:
        #         qs = qs.exclude(pk=self.instance.pk)

        #     if qs.exists():
        #         raise serializers.ValidationError(
        #             {
        #                 "start_at": _(
        #                     "This booking overlaps with another active booking."
        #                 )
        #             }
        #         )

        return attrs


class AgendaSerializerSimple(BaseModelSerializer):
    class Meta:
        model = Agenda
        fields = [
            "pk",
            "subid",
            "title",
            "customer_name",
            "start_at",
            "end_at",
            "status",
        ]


class AgendaCalendarSerializer(BaseModelSerializer):
    """
    Serializer for frontend calendar libraries such as FullCalendar.

    Output example:
    {
        "id": "abc123",
        "title": "Wedding Booking - John",
        "start": "2026-05-10T10:00:00+07:00",
        "end": "2026-05-10T14:00:00+07:00",
        "allDay": false,
        "color": "#3788d8",
        "extended_props": {...}
    }
    """

    start = serializers.DateTimeField(source="start_at", read_only=True)
    end = serializers.DateTimeField(source="end_at", read_only=True)
    allDay = serializers.BooleanField(source="all_day", read_only=True)
    extended_props = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        fields = [
            "pk",
            "title",
            "start",
            "end",
            "allDay",
            "color",
            "extended_props",
        ]

    def get_extended_props(self, obj):
        return {
            "pk": obj.subid,
            "customer_name": obj.customer_name,
            "customer_phone": obj.customer_phone,
            "customer_email": obj.customer_email,
            "location": obj.location,
            "status": obj.status,
            "source": obj.source,
            "duration_minutes": obj.duration_minutes,
            "event": EventSerializerSimple(obj.event).data if obj.event else None,
        }


class AgendaTableSerializer(BaseModelSerializer):
    """
    Serializer for admin table/list view.
    """

    event = serializers.SerializerMethodField()
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = Agenda
        fields = [
            "pk",
            "subid",
            "title",
            "customer_name",
            "customer_phone",
            "customer_email",
            "event",
            "location",
            "start_at",
            "end_at",
            "duration_minutes",
            "status",
            "source",
            "created",
            "updated",
        ]

    def get_event(self, obj):
        return EventSerializerSimple(obj.event).data if obj.event else None

    def get_duration_minutes(self, obj):
        return obj.duration_minutes