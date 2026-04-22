# core/middleware/tenant_middleware.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from services.tenant.models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):

        try:
            validated_token = self.jwt_auth.get_validated_token(
                self.jwt_auth.get_raw_token(self.jwt_auth.get_header(request))
            )

            tenant_id = validated_token.get("tenant_id")

            if tenant_id:
                request.tenant = Tenant.objects.get(id=tenant_id)

        except Exception:
            request.tenant = None

        return self.get_response(request)
