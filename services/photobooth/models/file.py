from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import get_subid_model
from services.account.models import User

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


class File(get_subid_model()):
    """
    Custom File model to group permissions.
    """

    event = models.ForeignKey("photobooth.Event", on_delete=models.CASCADE)
    session = models.ForeignKey("photobooth.Session", on_delete=models.CASCADE)
    # file = models.ForeignKey("file.File", on_delete=models.CASCADE)
    file = models.FileField(upload_to="photobooth/files/")

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)

    created = models.DateTimeField(_("created"), auto_now_add=True)
    updated = models.DateTimeField(_("updated"), auto_now=True)

    objects = FileManager()

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")

    def __str__(self) -> str:
        return f"Photobooth File {self.id}"
