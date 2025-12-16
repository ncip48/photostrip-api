from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TopupTransactionViewSet, TopupWebhookView

# --- Router for ViewSets ---
router = DefaultRouter()
router.register(r"", TopupTransactionViewSet, basename="topup")
# --- End Router ---

urlpatterns = [
    path("webhook/", TopupWebhookView.as_view(), name="topup-webhook"),
    path("", include(router.urls)),
]
