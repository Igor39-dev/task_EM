from rest_framework.views import APIView
from rest_framework.response import Response

from user_auth.authentications import JWTAuthentication
from products.models import Product
from access.permissions import check_permission

class ProductListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    def get(self, request):
        if not request.user:
            return Response({"detail": "Unauthorized"}, status=401)

        if not check_permission(request.user, 'products', 'read'):
            return Response({"detail": "Forbidden"}, status=403)

        products = Product.objects.all().values("id", "name", "price")
        return Response(list(products))
