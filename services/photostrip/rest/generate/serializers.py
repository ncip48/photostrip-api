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
        request = self.context["request"]

        photos = {}

        # Files
        for key, file in request.FILES.items():
            photos[key] = file

        # URLs / strings
        for key, value in request.data.items():
            if key.startswith("zone") and isinstance(value, str):
                photos.setdefault(key, value)

        if not photos:
            raise serializers.ValidationError("No photos provided")

        attrs["photos"] = photos
        return attrs
