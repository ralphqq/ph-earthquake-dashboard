from datetime import datetime

from django.db import models
import pytz


class Bulletin(models.Model):
    time_of_quake = models.DateTimeField(null=True)
    url = models.URLField(null=False, unique=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=4, decimal_places=1)
    magnitude = models.DecimalField(max_digits=3, decimal_places=1)
    location = models.CharField(max_length=2048, default='')

    class Meta:
        indexes = [
            models.Index(fields=['time_of_quake']),
            models.Index(fields=['url'])
        ]
        ordering = ['-time_of_quake']
    def __str__(self):
        return self.url
