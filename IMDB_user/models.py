from django.db import models
from movies.models import Movie
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyCustomUser(AbstractUser):
    displayname = models.CharField(max_length=30)
    watch_list = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return self.username
