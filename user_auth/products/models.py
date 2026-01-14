from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
