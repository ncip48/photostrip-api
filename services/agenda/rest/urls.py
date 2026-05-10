from django.urls import include, path

from .agenda import urls as agenda_urls

app_name = "agenda"

urlpatterns = [
    path("agenda/", include(agenda_urls)),
]
