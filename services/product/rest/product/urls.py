from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
