from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework import parsers, status
from rest_framework.response import Response

from core.common.viewsets import BaseViewSet
from services.gallery.models.gallery import Gallery
from services.gallery.rest.gallery.serializers import GallerySerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("GalleryViewSet",)


class GalleryViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = "subid"
    search_fields = []
    # required_perms = [
    #     "account.add_role",
    #     "account.change_role",
    #     "account.delete_role",
    #     "account.view_role",
    # ]
    my_tags = ["Galleries"]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_queryset(self):
        return self.queryset.owned(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
