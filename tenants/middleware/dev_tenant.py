from django_tenants.middleware.main import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name


class DevTenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, request):
        print("request :", request, type(request))
        host = request.split(":")[0]
        # host = request.META.get("HTTP_HOST", "").split(":")[0]
        if host in ["admin.localhost", "localhost"]:

            class PublicTenant:
                domain_url = host
                schema_name = get_public_schema_name()

            return PublicTenant()

        return super().get_tenant(domain_model, request)
