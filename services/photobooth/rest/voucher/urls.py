from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import VoucherViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"vouchers", VoucherViewSet, basename="voucher")
# --- End Router ---

urlpatterns = [
    path("", include(router.urls)),
]
