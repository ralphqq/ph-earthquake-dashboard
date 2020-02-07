from datetime import datetime

from django.db import models
from django.utils import timezone


class Bulletin(models.Model):
    time_of_quake = models.DateTimeField(null=True)
    url = models.URLField(null=False, unique=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    depth = models.DecimalField(max_digits=4, decimal_places=1)
    magnitude = models.DecimalField(max_digits=3, decimal_places=1)
    location = models.CharField(max_length=2048, default='')
    scraped_at = models.DateTimeField(default=None, blank=True, null=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['time_of_quake']),
            models.Index(fields=['url'])
        ]
        ordering = ['-time_of_quake']

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        """Overrides the built-in save method.

        This new method assigns the current time to the instance's 
        `scraped_at` and `updated_at` attributes when first saved, 
        then subsequently updates `update_at` accordingly.
        """
        current_time = timezone.now()
        if self.scraped_at is None:
            self.scraped_at = current_time
        self.updated_at = current_time
        super().save(*args, **kwargs)
