from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


"""
{
    "first_name": "user1",
    "last_name": "surname1",
    "middle_name": "midname1",
    "email": "user1@mail.com",
    "password": "123456"
}
"""
