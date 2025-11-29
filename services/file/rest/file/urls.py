from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FileViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"files", FileViewSet, basename="file")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
