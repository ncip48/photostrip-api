from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model
from services.account.models import User

import os
import uuid

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "FileQuerySet",
    "FileManager",
    "File",
)


class FileQuerySet(models.QuerySet):
    def owned(self, user: User) -> models.QuerySet:
        return self.filter(user=user)


_FileManagerBase = models.Manager.from_queryset(FileQuerySet)  # type: type[FileQuerySet]


class FileManager(_FileManagerBase):
    pass


def photobooth_file_upload_path(instance: File, filename: str) -> str:
    """
    Upload path:
    photobooth/files/:event_subid/:session_subid/:filename
    """

    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"

    event_subid = instance.event.subid if instance.event else "unknown_event"
    session_subid = instance.session.subid if instance.session else "unknown_session"

    return os.path.join(
        "photobooth",
        "files",
        event_subid,
        session_subid,
        filename,
    )


class File(get_subid_model()):
    """
    Custom File model to group permissions.
    """

    class Type(models.TextChoices):
        PHOTOSTRIP = "photostrip", "Photostrip"
        LIVE_VIDEO = "live_video", "Live Video"
        GIF = "gif", "GIF"
        DEFAULT = "default", "Default"

    event = models.ForeignKey("photobooth.Event", on_delete=models.CASCADE)
    session = models.ForeignKey("photobooth.Session", on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.DEFAULT)
    file = models.FileField(
        upload_to=photobooth_file_upload_path,
        max_length=500,
    )
    live_video = models.FileField(
        upload_to=photobooth_file_upload_path,
        null=True,
        blank=True,
        max_length=500,
    )

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = FileManager()

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self) -> str:
        return f"Photobooth File {self.id}"
