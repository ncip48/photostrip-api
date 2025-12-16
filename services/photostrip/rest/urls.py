from django.urls import include, path

from .photostrip import urls as photostrip_urls

app_name = "photostrip"

urlpatterns = [
    path("photostrip/", include(photostrip_urls)),
]
