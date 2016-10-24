from django.db import models
from django.contrib.auth.models import User

from website import settings

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    path = models.FileField(upload_to="videos/%Y/%m/%d")
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        title = 'title: ' + str(self.title)
        description = 'description: ' + str(self.description)
        path = 'path: ' + str(self.path)
        pub_date = 'pub_date: ' + str(self.pub_date)

        return '\n'.join([title, description, path, pub_date])

