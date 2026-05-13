from django.urls import include, path

from .plan import urls as photostrip_urls

app_name = "subscription"

urlpatterns = [
    path("subscription/", include(photostrip_urls)),
]
