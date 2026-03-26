from services.photobooth.models import File
import uuid
from pathlib import Path
from django.core.files import File as DjangoFile
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from services.photostrip.rest.generate.serializers import GeneratePhotostripSerializer
from services.photostrip.utils.generator import generate_photostrip


class GeneratePhotostripViewSet(ViewSet):
    parser_classes = [MultiPartParser, FormParser]

    # @action(detail=False, methods=["post"], url_path="generate")
    # def generate(self, request):
    #     serializer = GeneratePhotostripSerializer(
    #         data=request.data,
    #         context={"request": request},
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     template_id = serializer.validated_data["template_id"]
    #     photos = serializer.validated_data["photos"]

    #     filename = f"{template_id}_{uuid.uuid4().hex}.png"
    #     output_path = Path(settings.MEDIA_ROOT) / "photostrips" / filename

    #     result_path = generate_photostrip(
    #         template_id=template_id,
    #         photos=photos,
    #         output_path=output_path,
    #     )

    #     print(result_path)

    #     return Response(
    #         {
    #             "status": "success",
    #             "file": request.build_absolute_uri(
    #                 settings.MEDIA_URL + f"photostrips/{filename}"
    #             ),
    #         },
    #         status=status.HTTP_201_CREATED,
    #     )

    @action(detail=False, methods=["post"], url_path="generate")
    def generate(self, request):
        serializer = GeneratePhotostripSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        template_id = serializer.validated_data["template_id"]
        photos = serializer.validated_data["photos"]

        event = serializer.validated_data.get("event")
        session = serializer.validated_data.get("session")
        user = request.user

        filename = f"{template_id}_{uuid.uuid4().hex}.png"
        temp_path = Path(settings.MEDIA_ROOT) / "tmp" / filename

        # 1️⃣ Generate image
        generate_photostrip(
            template_subid=template_id,
            photos=photos,
            output_path=temp_path,
        )

        # 2️⃣ Save into File model
        with open(temp_path, "rb") as f:
            File.objects.create(
                event=event,
                session=session,
                user=user,
                file=DjangoFile(f, name=filename),
                type=File.Type.PHOTOSTRIP,
            )

        # 3️⃣ Optional: cleanup temp file
        temp_path.unlink(missing_ok=True)

        return Response(
            status=status.HTTP_201_CREATED,
        )
