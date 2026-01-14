import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication

from users.models import User


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'], is_active=True)
            return (user, None)
        except Exception:
            return None
