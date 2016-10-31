from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from friendship.models import Friend
from django.http import Http404

import json

from .models import Video, Message, Seen


def play(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    request.user.profile.currentlyWatching = True
    request.user.profile.save()
    seen = Seen.objects.create(video=video, user=request.user.profile)
    seen.save()
    try:
        last_chat_message = Message.objects.filter(video=video_id).last().pk
    except AttributeError:
        last_chat_message = -1

    return render(request, 'videochat/player.html',
                  {'video': video, 'last_chat_message': last_chat_message})


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


@login_required
def newchatmessage(request):
    if not request.POST:
        # Return HttpResponse with error
        pass

    try:
        video = Video.objects.filter(pk=request.POST.get('videopk')).first()
    except:
        # Video does not exist
        pass

    message = Message(
        text=request.POST.get('message'),
        author=request.user,
        video=video,
        )
    message.save()

    return HttpResponse(request.POST.get('message'))


@login_required
def getchatmessages(request):

    videopk = pk=request.GET.get('videopk')
    try:
        video = Video.objects.filter(videopk).first()
    except:
        # Video does not exist
        pass

    response = {}

    last_chat_message = request.GET.get('last_chat_message')
    response["last_chat_message"] = last_chat_message

    messages_queryset = Message.objects \
               .filter(pk__gt=last_chat_message) \
               .filter(video=videopk).order_by('-date_sent')

    if messages_queryset.last() != None:
        response["last_chat_message"] = messages_queryset.last().pk

    messages = messages_queryset.all()
    response["messages"] = []
    for m in messages:
        response["messages"].append({
                'text': m.text,
                'author': m.author.username,
               })
        
    return HttpResponse(json.dumps(response))
