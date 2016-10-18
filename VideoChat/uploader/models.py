from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    path = models.FileField(upload_to='videos/%Y/%m/%d/')
    duration = models.FloatField()
    pub_date = models.DateTimeField(auto_now = True)

