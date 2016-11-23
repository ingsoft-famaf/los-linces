from functools import wraps
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from friendship.models import Friend
from .ajax import delete_video
from .models import Video, Message, Seen, Chatroom, Event


def create_chatroom_if_not_provided(view_func):
    def _decorator(request, *args, **kwargs):
        video = get_object_or_404(Video, pk=kwargs['video_id'])
        if kwargs['chatroom_id'] == None:
            chatroom = Chatroom.objects.create(
                    video=video,
                    )
            chatroom.add_pause_event()

            return redirect(reverse('videochat:v',
                            args=[kwargs['video_id'], chatroom.pk]))
        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)


@login_required
@create_chatroom_if_not_provided
def play(request, video_id, chatroom_id=None):
    video = get_object_or_404(Video, pk=video_id)
    chatroom = get_object_or_404(Chatroom, pk=chatroom_id)

    chatroom.users.add(request.user)
    video.is_watched_by(request.user)
    last_message = chatroom.last_message()
    return render(request, 'videochat/player.html',
                  {'video': video, 'last_chat_message': last_message,
                   'chatroom': chatroom})


@login_required
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

    

@login_required
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

    chatroom = get_object_or_404(Chatroom, pk=request.POST.get('chatroom_id'))

    message = Message(
        text=clean_text(text=request.POST.get('message')),
        author=request.user,
        chatroom=chatroom,
        )
    message.save()

    return HttpResponse(request.POST.get('message'))

def clean_text(text):
    return text.replace("<", "&lt").replace(">", "&gt")

@login_required
def getchatmessages(request):

    chatroom = get_object_or_404(Chatroom, pk=request.GET.get('chatroom_id'))
    last_chat_message = request.GET.get('last_chat_message')

    response = {}

    messages = Message.objects \
               .filter(pk__gt=last_chat_message) \
               .filter(chatroom=chatroom).order_by('-date_sent') \
               .all()

    if messages.last() != None:
        last_chat_message = messages.last().pk

    response["last_chat_message"] = last_chat_message
    response["messages"] = [
        {
        'text': m.text,
        'author': m.author.username
        }
        for m in messages]
        
    return HttpResponse(json.dumps(response))
