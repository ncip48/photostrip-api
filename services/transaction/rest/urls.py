from django.urls import include, path

from .token import urls as token_urls
from .topup import urls as topup_urls

app_name = "transaction"

urlpatterns = [
    path("transaction/tokens/", include(token_urls)),
    path("transaction/topups/", include(topup_urls)),
]
