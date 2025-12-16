from django.urls import include, path

from .product import urls as product_urls

app_name = "product"

urlpatterns = [
    path("product/", include(product_urls)),
]
