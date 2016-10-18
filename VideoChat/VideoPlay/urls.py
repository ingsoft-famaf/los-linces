from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	# Example : /VideoPlay/35
	url(r'^(?P<video_id>[0-9]+)/$', views.play, name='play'),
]