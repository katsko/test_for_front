from django.db import models


class City(models.Model):
    scope_uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City)
    population = models.IntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ' ' + self.city.name
