from __future__ import annotations
from services.photostrip.utils.generator import generate_photostrip
from services.photostrip.rest.generate.serializers import GeneratePhotostripSerializer
import uuid
import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.common.viewsets import BaseViewSet
from services.photobooth.models.file import File
from services.photobooth.rest.file.serializers import FileSerializer

from io import BytesIO
from django.core.files.base import ContentFile

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

        template = serializer.validated_data["template"]
        photos = serializer.validated_data["photos"]

        event = serializer.validated_data.get("event")
        session = serializer.validated_data.get("session")
        user = request.user

        filename = f"{template.subid}_{uuid.uuid4().hex}.png"

        # 1️⃣ Generate image into memory buffer
        buffer = BytesIO()

        generate_photostrip(
            template_subid=template.subid,
            photos=photos,
            output_path=buffer,  # generator must support file-like object
        )

        buffer.seek(0)

        # 2️⃣ Save directly to MinIO via django-storages
        file = File.objects.create(
            event=event,
            session=session,
            user=user,
            file=ContentFile(buffer.read(), name=filename),
            type=File.Type.PHOTOSTRIP,
        )

        return Response(status=status.HTTP_201_CREATED, data=FileSerializer(file).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
