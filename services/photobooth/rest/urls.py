from django.urls import include, path

from .event import urls as event_urls
from .voucher import urls as voucher_urls

app_name = "photobooth"

urlpatterns = [
    path("photobooth/", include(event_urls)),
    path("photobooth/", include(voucher_urls)),
]
