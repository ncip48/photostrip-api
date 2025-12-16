from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PhotostripViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"photostrips", PhotostripViewSet, basename="photostrip")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
