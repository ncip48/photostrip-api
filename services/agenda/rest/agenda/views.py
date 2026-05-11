from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _
from rest_framework import parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet, TenantQuerysetMixin
from services.agenda.models import Agenda
from services.agenda.rest.agenda.serializers import (
    AgendaCalendarSerializer,
    AgendaSerializer,
    AgendaTableSerializer,
)

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("AgendaViewSet",)


class AgendaViewSet(TenantQuerysetMixin, BaseViewSet):
    """
    ViewSet for photobooth calendar event bookings.

    Features:
    - Admin manually creates booking
    - Admin updates booking
    - Admin deletes booking
    - Calendar view endpoint
    - Table view endpoint
    - Filter by date range, status, event, and search keyword
    """

    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    lookup_field = "subid"

    search_fields = [
        "title",
        "customer_name",
        "customer_phone",
        "customer_email",
        "location",
    ]

    ordering = ["start_at", "-id"]
    my_tags = ["Photobooth Event Bookings"]

    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    ]

    # Uncomment and adjust based on your permission system.
    # required_perms = [
    #     "photobooth.add_Agenda",
    #     "photobooth.change_Agenda",
    #     "photobooth.delete_Agenda",
    #     "photobooth.view_Agenda",
    # ]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("tenant", "event", "created_by")

        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        status_param = self.request.query_params.get("status")
        event = self.request.query_params.get("event")
        source = self.request.query_params.get("source")
        search = self.request.query_params.get("search")

        if start and end:
            start_dt = parse_datetime(start)
            end_dt = parse_datetime(end)

            if start_dt and end_dt:
                qs = qs.filter(
                    start_at__lt=end_dt,
                    end_at__gt=start_dt,
                )

        if status_param:
            qs = qs.filter(status=status_param)

        if event:
            qs = qs.filter(event_id=event)

        if source:
            qs = qs.filter(source=source)

        if search:
            qs = qs.filter(
                title__icontains=search
            ) | qs.filter(
                customer_name__icontains=search
            ) | qs.filter(
                customer_phone__icontains=search
            ) | qs.filter(
                customer_email__icontains=search
            ) | qs.filter(
                location__icontains=search
            )

        return qs.distinct()

    def perform_create(self, serializer):
        """
        Automatically assign creator when admin manually creates booking.
        If your TenantQuerysetMixin already injects tenant, keep it there.
        Otherwise, pass tenant here from request.user or request.tenant.
        """

        user = self.request.user if self.request.user.is_authenticated else None

        # If your project uses request.tenant, uncomment this:
        serializer.save(created_by=user, tenant=self.request.tenant)

    @action(detail=False, methods=["get"], url_path="calendar")
    def calendar(self, request, *args, **kwargs):
        """
        Calendar endpoint.

        Example:
        GET /api/photobooth/event-bookings/calendar/?start=2026-05-01T00:00:00+07:00&end=2026-05-31T23:59:59+07:00

        Good for frontend calendar UI.
        """
        qs = self.filter_queryset(self.get_queryset())
        serializer = AgendaCalendarSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="table")
    def table(self, request, *args, **kwargs):
        """
        Table endpoint.

        Example:
        GET /api/photobooth/event-bookings/table/?status=confirmed
        """
        qs = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = AgendaTableSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AgendaTableSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="cancel")
    def cancel(self, request, *args, **kwargs):
        """
        Shortcut endpoint to cancel booking.

        POST /api/photobooth/event-bookings/{subid}/cancel/
        """
        booking = self.get_object()
        booking.status = Agenda.BookingStatus.CANCELLED
        booking.save(update_fields=["status", "updated"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, *args, **kwargs):
        """
        Shortcut endpoint to mark booking as completed.

        POST /api/photobooth/event-bookings/{subid}/complete/
        """
        booking = self.get_object()
        booking.status = Agenda.BookingStatus.COMPLETED
        booking.save(update_fields=["status", "updated"])

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)