from django.db import models
from django.core.validators import MinValueValidator


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    path = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        title = 'title: ' + str(self.title)
        description = 'description: ' + str(self.description)
        path = 'path: ' + str(self.path)
        pub_date = 'pub_date: ' + str(self.pub_date)

        return '\n'.join([title, description, path, pub_date])
