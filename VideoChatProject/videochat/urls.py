from django.conf.urls import url
from . import views

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    url(r'^(?P<video_id>[0-9]+)/$', views.play, name='play'),
]
