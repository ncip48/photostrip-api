from django.urls import include, path

from .photostrip import urls as photostrip_urls
from .generate import urls as generate_urls

app_name = "photostrip"

urlpatterns = [
    path("photostrip/", include(photostrip_urls)),
    path("photostrip/", include(generate_urls)),
]
