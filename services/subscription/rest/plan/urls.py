from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionPlanViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"plans", SubscriptionPlanViewSet, basename="plan")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
