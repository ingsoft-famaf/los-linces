from haystack import indexes
from .models import Video
from django.contrib.auth.models import User


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    description = indexes.CharField(model_attr='description')
    path = indexes.CharField(model_attr='path')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Video

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
