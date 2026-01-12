# serializers.py
from core.common.serializers import BaseModelSerializer
from rest_framework import serializers
from services.activity.models import Activity

class ActivitySerializer(BaseModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "pk",
            "activity",
            "references",
            "model",
            "user",
            "created",
            "updated",
        ]
