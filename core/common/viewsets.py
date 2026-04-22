from django.contrib.auth import get_user_model
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from core.common.paginations import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied

from core.common.permissions import HasRolePermission

User = get_user_model()


class BaseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and managing superusers.
    Only accessible by superusers.
    Includes filter, search, ordering, and pagination.
    """

    permission_classes = [IsAuthenticated, HasRolePermission]

    # Enable filtering, searching, ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # ✅ Filtering by fields
    filterset_fields = []

    # ✅ Searching (case-insensitive)
    search_fields = []

    # ✅ Ordering
    ordering_fields = ["created"]
    ordering = ["-created"]

    # ✅ Pagination
    pagination_class = PageNumberPagination


class TenantQuerysetMixin:
    def get_queryset(self):
        user = self.request.user
        tenant = getattr(self.request, "tenant", None)

        queryset = super().get_queryset()

        if user.is_superuser:
            return queryset

        if tenant:
            return queryset.filter(tenant=tenant)

        return queryset.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_superuser:
            serializer.save()
            return

        tenant = getattr(self.request, "tenant", None)

        if tenant is None:
            raise PermissionDenied("Tenant missing from request")

        serializer.save(tenant=tenant)

    def perform_update(self, serializer):
        user = self.request.user

        if user.is_superuser:
            serializer.save()
            return

        # tenant should NOT change after creation
        serializer.save()
