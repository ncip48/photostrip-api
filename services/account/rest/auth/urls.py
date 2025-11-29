from django.urls import path

from .views import LoginView, RefreshView, RegisterView, profile

urlpatterns = [
    # Profile endpoint
    path("profile/", profile, name="user-profile"),
    # Auth endpoints
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterView.as_view(), name="register"),
    path("refresh/", RefreshView.as_view(), name="token_refresh"),
]
