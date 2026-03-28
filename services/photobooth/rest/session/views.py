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

    def get_queryset(self):
        if self.action == "files":
            return self.queryset

        return self.queryset.owned(user=self.request.user)

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
        file_type = request.query_params.get("type")
        session = self.get_object()
        files = session.file_set.all()
        if file_type:
            files = files.filter(type=file_type)
        return Response(
            FileSerializer(files, many=True, context={"request": request}).data
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="files/(?P<file_subid>[^/.]+)",
    )
    def delete_file(self, request, subid=None, file_subid=None):
        session = self.get_object()
        file_obj = session.file_set.get(subid=file_subid)

        # delete file from S3
        if file_obj.file:
            file_obj.file.delete(save=False)

        # delete database record
        file_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
