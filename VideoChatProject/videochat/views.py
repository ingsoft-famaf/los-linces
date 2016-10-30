from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from friendship.models import Friend

import json

from .models import Video, Message


def play(request, video_id):
    video = get_object_or_404(Video, pk=video_id)
    return render(request, 'videochat/player.html', {'video': video})


def user(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)

    if Friend.objects.are_friends(request.user, other_user) or (request.user == other_user):
        friend_requests = Friend.objects.unread_requests(user=other_user)

        return render(request, 'videochat/user.html', {'user': other_user,
                                                       'friend_requests': friend_requests})
    else:
        return render(request, 'videochat/friend_request.html', {'user': other_user, 'me': request.user})


def friend(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    if not((Friend.objects.are_friends(request.user, other_user)) or(request.user == other_user)):
        Friend.objects.add_friend(request.user, other_user)
        return render(request, 'videochat/request_sent.html', {'user': other_user})
    else:
        return render(request, 'videochat/user.html', {'user': other_user})

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
    if not request.POST:
        # Return HttpResponse with error
        pass

    videopk = pk=request.POST.get('videopk')
    try:
        video = Video.objects.filter(videopk).first()
    except:
        # Video does not exist
        pass

    mm = {}
    last_message_received = int(request.POST.get('lastmessagereceived'))

    if last_message_received > 0:
        messages = Message.objects.filter(pk__gt=last_message_received) \
                   .filter(video=videopk).all()
    else:
        # Get all/some messages
        messages = Message.objects.order_by('-date_sent').all()[:5]

    for m in messages:
        mm[m.pk] = {'pk': m.pk,
                    'text': m.text,
                    'author': m.author.username,
                   }

    return HttpResponse(json.dumps(mm))

