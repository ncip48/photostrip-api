from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SessionViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"sessions", SessionViewSet, basename="session")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
