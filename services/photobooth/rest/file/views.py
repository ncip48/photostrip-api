from __future__ import annotations
from services.photostrip.utils.generator import generate_photostrip
from services.photostrip.rest.generate.serializers import GeneratePhotostripSerializer
import uuid
from pathlib import Path
from django.core.files import File as DjangoFile
from django.conf import settings
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
    filterset_fields = [
        "type",
    ]
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

    @action(detail=False, methods=["post"], url_path="generate-photostrip")
    def generate_photostrip(self, request):
        serializer = GeneratePhotostripSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        template_id = serializer.validated_data["template_id"]
        photos = serializer.validated_data["photos"]

        event = serializer.validated_data.get("event")
        session = serializer.validated_data.get("session")
        user = request.user

        filename = f"{template_id}_{uuid.uuid4().hex}.png"
        temp_path = Path(settings.MEDIA_ROOT) / "tmp" / filename

        # 1️⃣ Generate image
        generate_photostrip(
            template_id=template_id,
            photos=photos,
            output_path=temp_path,
        )

        # 2️⃣ Save into File model
        with open(temp_path, "rb") as f:
            File.objects.create(
                event=event,
                session=session,
                user=user,
                file=DjangoFile(f, name=filename),
                type=File.Type.PHOTOSTRIP,
            )

        # 3️⃣ Optional: cleanup temp file
        temp_path.unlink(missing_ok=True)

        return Response(
            status=status.HTTP_201_CREATED,
        )
