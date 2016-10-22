from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ... the rest of your URLconf goes here ...
	url(r'^(?P<video_id>[0-9]+)/$', views.play, name='play'),
]
