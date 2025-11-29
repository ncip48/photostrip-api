from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "FileQuerySet",
    "FileManager",
    "File",
)


class FileQuerySet(models.QuerySet):
    pass


_FileManagerBase = models.Manager.from_queryset(FileQuerySet)  # type: type[FileQuerySet]


class FileManager(_FileManagerBase):
    pass


class File(get_subid_model()):
    """
    Custom File model to group permissions.
    """

    encrypted_file = models.FileField(upload_to="secure_images/")

    # Metadata required for decryption
    encryption_iv = models.CharField(max_length=255)
    encrypted_key = models.TextField()  # In production, this is encrypted with RSA

    # Store mimetype (e.g., 'image/png') so the browser knows how to render it
    mime_type = models.CharField(max_length=50, default="image/jpeg")

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = FileManager()

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("files")

    def __str__(self) -> str:
        return f"Encrypted Image {self.id}"
