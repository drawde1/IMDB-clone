from django.db import models

# Create your models here.


class Movie(models.Model):
    imbd_id = models.CharField(max_length=20)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.imbd_id
