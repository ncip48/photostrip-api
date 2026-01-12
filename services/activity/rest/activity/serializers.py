# serializers.py
from services.account.rest.user.serializers import ProfileSerializer
from core.common.serializers import BaseModelSerializer
from rest_framework import serializers
from services.activity.models import Activity

class ActivitySerializer(BaseModelSerializer):
    user = ProfileSerializer()
    
    class Meta:
        model = Activity
        fields = [
            "pk",
            "activity",
            "reference",
            "model",
            "user",
            "created",
            "updated",
        ]
