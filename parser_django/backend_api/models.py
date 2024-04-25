from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    position = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.email