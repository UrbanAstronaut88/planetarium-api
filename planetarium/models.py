from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class ShowTheme(models.Model):
    name = models.CharField(max_length=100)
    shows = models.ManyToManyField(AstronomyShow, related_name="themes")

    def __str__(self):
        return self.name
