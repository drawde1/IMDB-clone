from django.db import models
from movies.models import Movie
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyCustomUser(AbstractUser):
    karma_score = models.IntegerField(default=0)
    displayname = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    watch_list = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='watch'
    )
    favorites_list = models.ManyToManyField(
        Movie,
        blank=True,
        related_name='favorites'
    )
    followed_list = models.ManyToManyField(
        'self',
        blank=True,
        related_name='followed',
        symmetrical=False

    )
    REQUIRED_FIELDS = ['displayname']

    @property
    def emoji(self):
        if self.karma_score > 500:
            return '🤩'
        elif self.karma_score > 200:
            return '😋'
        elif self.karma_score >= 0:
            return '😶'
        elif self.karma_score < 0:
            return '😫'
        elif self.karma_score < -100:
            return '🤬'

    def __str__(self):
        return self.username
