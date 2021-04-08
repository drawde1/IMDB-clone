from django.db import models

# Create your models here.


class Movie(models.Model):
    tmdb_id = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=50, default='')
    poster_url = models.URLField(default='')

    def __str__(self):
        return self.name
