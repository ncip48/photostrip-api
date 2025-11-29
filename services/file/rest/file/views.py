from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework import parsers, status
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet
from services.file.models import File
from services.file.rest.file.serializers import FileSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("FileViewSet",)


class FileViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = "subid"
    search_fields = []
    # required_perms = [
    #     "account.add_role",
    #     "account.change_role",
    #     "account.delete_role",
    #     "account.view_role",
    # ]
    my_tags = ["Files"]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
