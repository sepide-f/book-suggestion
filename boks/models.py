from django.db import models
from users.models import CustomUser


class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return self.rating
