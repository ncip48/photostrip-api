from __future__ import annotations
from services.photobooth.rest.file.serializers import FileSerializer

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from core.common.viewsets import BaseViewSet
from services.photobooth.models.session import Session
from services.photobooth.rest.session.serializers import SessionSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("SessionViewSet",)


class SessionViewSet(BaseViewSet):
    """
    ViewSet for managing Photobooth Sessions.
    """

    queryset = Session.objects.select_related("event", "voucher")
    serializer_class = SessionSerializer
    lookup_field = "subid"
    search_fields = []
    my_tags = ["Photobooth Sessions"]

    def perform_create(self, serializer):
        """
        Assign session owner automatically.
        """
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[AllowAny],
    )
    def files(self, request, subid=None):
        """
        List files for a session.
        """
        session = self.get_object()
        files = session.file_set.all()
        return Response(FileSerializer(files, many=True, context={"request": request}).data)