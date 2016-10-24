from django.shortcuts import render, get_object_or_404
from .models import Video
from django.contrib.auth.models import User


def play(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'videochat/player.html', {'video': video})


def user(request, user_id):
    u = get_object_or_404(User, pk=user_id)
    return render(request, 'videochat/user.html', {'user': u})
