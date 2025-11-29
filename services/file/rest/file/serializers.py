from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.common.serializers import BaseModelSerializer
from services.file.models import File

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("FileSerializer",)


class FileSerializer(BaseModelSerializer):
    class Meta:
        model = File
        fields = [
            "pk",
            "encrypted_file",
            "encryption_iv",
            "encrypted_key",
            "mime_type",
            "created",
        ]
