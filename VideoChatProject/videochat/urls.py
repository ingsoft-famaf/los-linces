from django.conf.urls import url
from . import views
from . import ajax
app_name = 'videochat'

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    url(r'^ajax/add/$', ajax.add_friend),
    url(r'^ajax/cancel_fr/$', ajax.cancel_fr),
    url(r'^ajax/handle_request/$', ajax.handle_request),
    url(r'^u/(?P<user_id>[0-9]+)/$', views.user, name='u'),
    url(r'^v/(?P<video_id>[0-9]+)/$', views.play, name='v'),
    url(r'^fr/(?P<user_id>[0-9]+)/$', views.friendship_requests, name='fr'),
]
