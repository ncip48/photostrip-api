from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GeneratePhotostripViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"", GeneratePhotostripViewSet, basename="generate")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
