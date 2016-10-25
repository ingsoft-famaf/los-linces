from django.shortcuts import render, get_object_or_404
from .models import Video
from django.contrib.auth.models import User
from friendship.models import Friend


def play(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'videochat/player.html', {'video': video})


def user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if Friend.objects.are_friends(request.user, other_user) or (request.user == other_user):
        return render(request, 'videochat/user.html', {'user': other_user})
    else:
        return render(request, 'videochat/friend_request.html', {'user': other_user, 'me': request.user})


def friend(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if not((Friend.objects.are_friends(request.user, other_user)) or(request.user == other_user)):
        Friend.objects.add_friend(request.user, other_user)
        return render(request, 'videochat/request_sent.html', {'user': other_user})
    else:
        return render(request, 'videochat/user.html', {'user': other_user})
