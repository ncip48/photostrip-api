from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GalleryViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"galleries", GalleryViewSet, basename="gallery")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
