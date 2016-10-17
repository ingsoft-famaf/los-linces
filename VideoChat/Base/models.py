from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    path = models.CharField(max_length=200)
    duration = models.FloatField()
    pub_date = models.DateTimeField('date published')

