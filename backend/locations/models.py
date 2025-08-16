from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()
    market_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
