from django.conf.urls import url
from django.conf.urls.static import static
from django.conf  import settings
from . import views

urlpatterns = [
	# Example : /VideoPlay/35
	url(r'^(?P<video_id>[0-9]+)/$', views.play, name='play'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
