from django.db import models

# Create your models here.


class Actor(models.Model):
    imbd_id = models.CharField(max_length=20)
    name = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0)
    bio = models.CharField(max_length=280)


    def __str__(self):
        return self.imbd_id