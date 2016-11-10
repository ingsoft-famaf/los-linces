from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from friendship.models import Friend
from .ajax import delete_video

import json

from .models import Video, Message, Seen, Chatroom


def play(request, video_id, chatroom_id):
    video = get_object_or_404(Video, pk=video_id)
    if chatroom_id == None:
        chatroom = Chatroom.objects.create(
                state=Chatroom.PLAY_STATE,
                video=video,
                )
        chatroom.save()
        return redirect(reverse('videochat:v', args=[video_id, chatroom.pk]))

    chatroom = get_object_or_404(Chatroom, pk=chatroom_id)
    chatroom.users.add(request.user)
    request.user.profile.currentlyWatching = True
    request.user.profile.save()
    seen = Seen.objects.create(video=video, user=request.user.profile)
    seen.save()
    last_message = Message.objects.filter(chatroom=chatroom).last()
    if last_message is not None:
        last_chat_message = last_message.pk
    else:
        last_chat_message = -1

    return render(request, 'videochat/player.html',
                  {'video': video, 'last_chat_message': last_chat_message,
                   'chatroom': chatroom})


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
        chatroom = get_object_or_404(Chatroom, pk=request.POST.get('chatroompk'))
    except:
        # Video does not exist
        pass

    message = Message(
        text=request.POST.get('message'),
        author=request.user,
        chatroom=chatroom,
        )
    message.save()

    return HttpResponse(request.POST.get('message'))


@login_required
def getchatmessages(request):

    chatroompk = pk=request.GET.get('chatroompk')

    try:
        chatroom = Chatroom.objects.filter(chatroompk).first()
    except:
        # Chatroom does not exist
        pass

    response = {}

    last_chat_message = request.GET.get('last_chat_message')
    response["last_chat_message"] = last_chat_message

    messages_queryset = Message.objects \
               .filter(pk__gt=last_chat_message) \
               .filter(chatroom=chatroompk).order_by('-date_sent')

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
