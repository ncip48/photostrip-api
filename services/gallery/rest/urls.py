from django.urls import include, path

from .gallery import urls as gallery_urls

app_name = "gallery"

urlpatterns = [
    path("gallery/", include(gallery_urls)),
]
