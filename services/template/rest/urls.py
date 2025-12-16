from django.urls import include, path

from .template import urls as photostrip_urls

app_name = "template"

urlpatterns = [
    path("template/", include(photostrip_urls)),
]
