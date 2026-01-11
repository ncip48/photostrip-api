from rest_framework.routers import DefaultRouter

from .views import DashboardStatsViewSet

router = DefaultRouter()
router.register(r"stats", DashboardStatsViewSet, basename="stats")

urlpatterns = router.urls
