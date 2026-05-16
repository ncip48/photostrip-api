from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.db import transaction

# from rest_framework import serializers
from core.common.serializers import BaseModelSerializer
from services.template.models import Dropzone, Template, TemplateSize
import json

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TemplateSerializer", "TemplateSizeSerializer", "DropzoneSerializer")


class TemplateSizeSerializer(BaseModelSerializer):
    class Meta:
        model = TemplateSize
        fields = ["width_photostrip", "height_photostrip"]


class DropzoneSerializer(BaseModelSerializer):
    class Meta:
        model = Dropzone
        fields = ["pk", "top", "left", "width", "height"]


class TemplateSerializer(BaseModelSerializer):
    size = TemplateSizeSerializer()
    dropzones = DropzoneSerializer(many=True)

    class Meta:
        model = Template
        fields = [
            "pk",
            "type",
            "name",
            "location",
            "size",
            "dropzones",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields["location"].required = False

    def to_internal_value(self, data):
        if hasattr(data, "dict"):
            data = data.dict()
        else:
            data = data.copy()

        # 🔥 FIX: parse JSON string
        if isinstance(data.get("size"), str):
            try:
                data["size"] = json.loads(data["size"])
            except Exception:
                pass

        if isinstance(data.get("dropzones"), str):
            try:
                data["dropzones"] = json.loads(data["dropzones"])
            except Exception:
                pass

        return super().to_internal_value(data)

    @transaction.atomic
    def create(self, validated_data):
        # 1. Separate nested data
        size_data = validated_data.pop("size", None)
        dropzones_data = validated_data.pop("dropzones", [])
        tenant = validated_data.pop("tenant", None)

        # 2. Create the Template instance
        template = Template.objects.create(tenant=tenant, **validated_data)

        # 3. Create Size (if exists)
        if size_data:
            TemplateSize.objects.create(template=template, **size_data)

        # 4. Create Dropzones
        for dz_data in dropzones_data:
            Dropzone.objects.create(template=template, **dz_data)

        return template

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Separate nested data
        size_data = validated_data.pop("size", None)
        dropzones_data = validated_data.pop("dropzones", None)

        # 2. Update the main Template fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 3. Handle 'Size' (One-to-One relationship)
        if size_data is not None:
            # We use update_or_create logic here
            # Assuming 'template.size' is how you access the related object
            if hasattr(instance, "size") and instance.size:
                for attr, value in size_data.items():
                    setattr(instance.size, attr, value)
                instance.size.save()
            else:
                # If it didn't exist before, create it now
                TemplateSize.objects.create(template=instance, **size_data)

        # 4. Handle 'Dropzones' (One-to-Many relationship)
        # STRATEGY: Replace All.
        # Since the form sends a fresh list without IDs, we delete old ones and create new ones.
        if dropzones_data is not None:
            # Clear existing dropzones related to this template
            instance.dropzones.all().delete()

            # Re-create them from the payload
            new_dropzones = []
            for dz_data in dropzones_data:
                # We do not save immediately to optimize if needed, but simple create is fine
                new_dropzones.append(Dropzone(template=instance, **dz_data))

            # Bulk create is more efficient than a loop of .create()
            Dropzone.objects.bulk_create(new_dropzones)

        return instance
