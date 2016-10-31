from django.shortcuts import render, get_object_or_404
from .models import Video, Seen
from django.contrib.auth.models import User, Permission
from website import settings
from friendship.models import Friend
from django.http import Http404


def play(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    request.user.profile.currentlyWatching = True
    request.user.profile.save()
    seen = Seen.objects.create(video=video, user=request.user.profile)
    seen.save()
    return render(request, 'videochat/player.html', {'video': video})


def user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    same_user = True
    if request.user != other_user:
        same_user = False

    friends = Friend.objects.friends(user=other_user)
    videos = Video.objects.filter(author=other_user)
    
    return render(request, 'videochat/user.html', {'user': other_user,
                                                   'friends': friends,
                                                   'same_user': same_user,
                                                   'videos': videos,
                                                   })

    

def friendship_requests(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if request.user == other_user:
        friend_requests = Friend.objects.unread_requests(user=other_user)
        return render(request, 'videochat/friendship_requests.html', {'user': other_user,
                                                                      'friend_requests': friend_requests, })
    else:
        return Http404


