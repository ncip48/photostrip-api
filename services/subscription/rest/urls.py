from django.urls import include, path

from .plan import urls as plan_urls
from .subscription import urls as subscription_urls

app_name = "subscription"

urlpatterns = [
    path("subscription/", include(plan_urls)),
    path("subscription/", include(subscription_urls)),
]
