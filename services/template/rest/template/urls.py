from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TemplateViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"templates", TemplateViewSet, basename="template")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
