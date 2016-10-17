from django.db import models
from django.core.validators import MinValueValidator


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    path = models.CharField(max_length=200)
    duration = models.FloatField(validators=[MinValueValidator(0)])
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        title = "title: " + str(self.title)
        description = "description: " + str(self.description)
        path = "path: " + str(self.path)
        duration = "duration: " + str(self.duration)
        pub_date = "pub_date: " + str(self.pub_date)

        return '\n'.join([title, description, path, duration, pub_date])


