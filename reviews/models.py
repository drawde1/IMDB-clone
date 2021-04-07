from django.db import models
from django.utils import timezone
from movies.models import Movie
from IMDB_user.models import MyCustomUser
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(
        MyCustomUser, on_delete=models.CASCADE, related_name='custom_user')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='movie')
    text = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)


    def __str__(self):
        return f'review: {self.id}'

    @property
    def vote_total(self):
        return self.upvote - self.downvote
