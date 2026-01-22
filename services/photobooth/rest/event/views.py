from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet
from services.photobooth.models.event import Event
from services.photobooth.rest.event.serializers import EventSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("EventViewSet",)


class EventViewSet(BaseViewSet):
    """
    ViewSet for managing Photobooth Events.
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = "subid"
    search_fields = ["title", "subtitle"]
    my_tags = ["Photobooth Events"]

    def get_queryset(self):
        """
        Only return events owned by the authenticated user.
        """
        return self.queryset.owned(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign event owner.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def default(self, request):
        # get default event by first event
        event = Event.objects.first()
        if event:
            return Response(EventSerializer(event, context={"request": request}).data)
        return Response({"message": "No default event found"}, status=404)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        """
        Event summary for current user.
        """
        qs = self.get_queryset()
        total_events = qs.count()
        paid_events = qs.filter(is_paid_event=True).count()
        free_events = qs.filter(is_paid_event=False).count()

        return Response(
            {
                "total_events": total_events,
                "paid_events": paid_events,
                "free_events": free_events,
            }
        )
