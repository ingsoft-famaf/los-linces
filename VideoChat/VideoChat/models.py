from django.db import models

class UploadFileModel(models.Model):
  video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
  
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    path = models.CharField(max_length=200)
    duration = models.FloatField()
    pub_date = models.DateTimeField('date published')

