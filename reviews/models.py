from django.db import models
from django.utils import timezone
from movies.models import Movie
from IMDB_user.models import MyCustomUser
# Create your models here.


class Vote(models.Model):
    value = models.IntegerField(default=1)


class Review(models.Model):
    user = models.ForeignKey(
        MyCustomUser, on_delete=models.CASCADE, related_name='custom_user')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='movie')
    text = models.TextField()
    creation_time = models.DateTimeField(default=timezone.now)
    votes = models.ManyToManyField(Vote)
    likedby = models.ManyToManyField(MyCustomUser)

    def __str__(self):
        return f'review: {self.id}'

    @property
    def vote_total(self):
        value = 0
        for vote in self.votes.all():
            value += vote.value
        return value
