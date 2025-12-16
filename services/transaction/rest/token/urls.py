from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TokenTransactionViewSet

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"", TokenTransactionViewSet, basename="token")
# --- End Router ---

urlpatterns = [
    path(
        "summary/",
        TokenTransactionViewSet.as_view({"get": "summary"}),
        name="token-transaction-summary",
    ),
    path("", include(router.urls)),
]
