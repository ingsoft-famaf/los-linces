from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	# Example : /VideoPlay/35
	url(r'^(?P<video_id>[0-9]+)/$', TemplateView.as_view(template_name="reproductor.html"), name='play'),
]