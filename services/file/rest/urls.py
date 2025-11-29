from django.urls import include, path

from .file import urls as file_urls

app_name = "file"

urlpatterns = [
    path("file/", include(file_urls)),
]
