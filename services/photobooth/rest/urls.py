from django.urls import include, path

from .event import urls as event_urls

app_name = "photobooth"

urlpatterns = [
    path("photobooth/", include(event_urls)),
]
