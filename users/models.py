from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    email = None

    def __str__(self):
        return self.username
