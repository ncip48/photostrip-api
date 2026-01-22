from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.common.viewsets import BaseViewSet
from services.photobooth.models.file import File
from services.photobooth.rest.file.serializers import FileSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("FileViewSet",)


class FileViewSet(BaseViewSet):
    """
    ViewSet for managing Photobooth Files.
    """

    queryset = File.objects.select_related("event", "session")
    serializer_class = FileSerializer
    lookup_field = "subid"
    search_fields = []
    my_tags = ["Photobooth Files"]

    def get_queryset(self):
        """
        Only files owned by current user.
        """
        return self.queryset.owned(user=self.request.user)

    def perform_create(self, serializer):
        """
        Assign file owner automatically.
        """
        serializer.save(user=self.request.user)
    