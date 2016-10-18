from django.db import models
from django.core.validators import MinValueValidator
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('es_index_name', 'es_type_name', 'es_mapping')


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    path = models.CharField(max_length=200)
    duration = models.FloatField(validators=[MinValueValidator(0)])
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        title = 'title: ' + str(self.title)
        description = 'description: ' + str(self.description)
        path = 'path: ' + str(self.path)
        duration = 'duration: ' + str(self.duration)
        pub_date = 'pub_date: ' + str(self.pub_date)

        return '\n'.join([title, description, path, duration, pub_date])

    class Meta:
        es_index_name = 'django'
        es_type_name = 'video'
        es_mapping = {
            'properties': {
                'title': {'type': 'string', 'analyzer': 'english'},
                'description': {'type': 'string', 'analyzer': 'english'},
                'path': {'type': 'string', 'index': 'no'},
                'duration': {'type': 'float', 'index': 'no'}
            }
        }
