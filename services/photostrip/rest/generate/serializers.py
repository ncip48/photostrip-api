from services.photobooth.models import Session, Event
from rest_framework import serializers


class GeneratePhotostripSerializer(serializers.Serializer):
    template_id = serializers.CharField()
    event = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Event.objects.all(),
        required=True,
    )
    session = serializers.SlugRelatedField(
        slug_field="subid",
        queryset=Session.objects.all(),
        required=True,
    )

    def validate(self, attrs):
        """
        Collect all uploaded files dynamically as zones
        """
        request = self.context["request"]
        files = request.FILES

        if not files:
            raise serializers.ValidationError("No photos uploaded")

        attrs["photos"] = files
        return attrs
