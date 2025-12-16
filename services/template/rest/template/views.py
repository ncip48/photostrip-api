from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework import parsers

from core.common.viewsets import BaseViewSet
from services.template.models.template import Template
from services.template.rest.template.serializers import TemplateSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TemplateViewSet",)


class TemplateViewSet(BaseViewSet):
    """
    A viewset for viewing and editing roles.
    Accessible only by superusers.
    """

    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    lookup_field = "subid"
    search_fields = []
    # required_perms = [
    #     "account.add_role",
    #     "account.change_role",
    #     "account.delete_role",
    #     "account.view_role",
    # ]
    my_tags = ["Templates"]
    ordering = ["-id"]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
