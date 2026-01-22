from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EventViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
