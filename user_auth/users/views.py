import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import User

def generate_token(user):
    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


class RegisterView(APIView):
    def post(self, request):
        password = bcrypt.hashpw(request.data['password'].encode(), bcrypt.gensalt())
        User.objects.create(
            email=request.data['email'],
            password_hash=password.decode(),
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
        )
        return Response({'status': 'registered'})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=401)

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return Response({"detail": "Invalid credentials"}, status=401)

        token = generate_token(user)

        response = Response({"status": "ok"})
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=2 * 60 * 60
        )
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response({"status": "ok"})
        response.delete_cookie('access_token')
        return response
