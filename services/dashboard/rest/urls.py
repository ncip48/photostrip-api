from django.urls import include, path

from .dashboard import urls as dashboard_urls

app_name = "dashboard"

urlpatterns = [
    path("dashboard/", include(dashboard_urls)),
]
