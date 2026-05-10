from django.urls import include, path
from rest_framework.routers import DefaultRouter
from services.agenda.rest.agenda.views import AgendaViewSet

router = DefaultRouter()

router.register(
    r"agendas",
    AgendaViewSet,
    basename="agenda",
)

urlpatterns = [
    path("", include(router.urls)),
]