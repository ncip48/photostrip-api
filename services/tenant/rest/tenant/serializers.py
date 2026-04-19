from __future__ import annotations
import os
from rest_framework import serializers
from typing import TYPE_CHECKING
from django.utils.translation import gettext_lazy as _
import logging
from core.common.serializers import BaseModelSerializer
from services.tenant.models.tenant import Tenant

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = ("TenantSerializer",)


class TenantSerializer(BaseModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Tenant
        fields = [
            "pk",
            "name",
            "photo",
            "is_active",
            "created",
            "updated",
        ]
        read_only_fields = ("created", "updated")

    def create(self, validated_data):
        photo_file = validated_data.pop("photo", None)
        tenant = Tenant.objects.create(**validated_data)

        if photo_file:
            tenant.upload_photo(photo_file)

        return tenant

    def update(self, instance, validated_data):
        photo_file = validated_data.pop("photo", None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace photo if new one is provided
        if photo_file:
            if instance.photo and instance.photo.name:
                # Remove old photo file from storage
                old_path = instance.photo.path
                if os.path.isfile(old_path):
                    os.remove(old_path)
            instance.upload_photo(photo_file)

        return instance


class TenantSerializerSimple(BaseModelSerializer):
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Tenant
        fields = [
            "pk",
            "name",
            "photo",
            "is_active",
        ]
        read_only_fields = ("created", "updated")
