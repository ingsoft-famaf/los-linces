from functools import wraps
import json

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from friendship.models import Friend, FriendshipRequest
from .models import Video, Event, Chatroom


def check_if_ajax(view_func):
    def _decorator(request, *args, **kwargs):
        if request.is_ajax() and request.POST:
            response = view_func(request, *args, **kwargs)
            return response
        else:
            return Http404
    return wraps(view_func)(_decorator)


@csrf_exempt
@check_if_ajax
def get_last_event(request):
    chatroom = get_object_or_404(Chatroom, pk=request.POST.get('chatroom_id'))
    event = Event.objects.filter(chatroom=chatroom).last()
    data = {'event_type': event.event_type,
            'relative_time': event.relative_time,
            # TODO return time as real time string
            'time': str(event.time),
           }
    return HttpResponse(json.dumps(data), content_type='application/json') 


@csrf_exempt
@check_if_ajax
def handle_events(request):
    event_type = request.POST.get('event_type')
    chatroom = get_object_or_404(Chatroom, pk=request.POST.get('chatroom_id'))
    if event_type == 'pause':
        chatroom.add_pause_event()
    elif event_type == 'play':
        chatroom.add_play_event()
    else:
        return Http404

    data = {'message': "event {} created".format(event_type)}
    return HttpResponse(json.dumps(data), content_type='application/json') 

@csrf_exempt
@check_if_ajax
def delete_friend(request):
    from_user = User.objects.get(pk=request.POST.get('from_user'))
    to_user = User.objects.get(pk=request.POST.get('to_user'))

    Friend.objects.remove_friend(from_user=from_user, to_user=to_user)

    data = {'message': "{} deleted".format(request.POST.get('to_user'))}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@check_if_ajax
def delete_video(request):
    video = Video.objects.get(pk=request.POST.get('video_pk'))
    current_user = User.objects.get(pk=request.POST.get('user_pk'))

    if current_user == video.author:
        video.delete()
    else:
        return Http404

    data = {'message': "{} deleted".format(request.POST.get('video_pk'))}
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@check_if_ajax
def finish_watching(request):
    current_user = User.objects.get(pk=request.POST.get('user'))

    current_user.profile.currentlyWatching = False
    current_user.profile.save()
    data = {'message': "{} finished watching a video".format(request.POST.get('user'))}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@check_if_ajax
def add_friend(request):
    from_user = User.objects.get(pk=request.POST.get('from_user'))
    to_user = User.objects.get(pk=request.POST.get('to_user'))

    Friend.objects.add_friend(from_user, to_user)
    data = {'message': "{} added".format(request.POST.get('to_user'))}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@check_if_ajax
def cancel_fr(request):
    from_user = User.objects.get(pk=request.POST.get('from_user'))
    to_user = User.objects.get(pk=request.POST.get('to_user'))

    FriendshipRequest.objects.get(from_user=from_user, to_user=to_user).delete()
    data = {'message': "{} friendship request deleted".format(request.POST.get('to_user'))}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
@check_if_ajax
def handle_request(request):
    to_user = User.objects.get(pk=request.POST.get('to_user'))
    from_user = User.objects.get(pk=request.POST.get('from_user'))

    friendship_request = FriendshipRequest.objects.get(from_user=from_user, to_user=to_user)

    ans = 'accepted'
    if request.POST.get('result') == 'true':
        friendship_request.accept()
    else:
        friendship_request.reject()
        FriendshipRequest.objects.get(from_user=from_user, to_user=to_user).delete()
        ans = "rejected"

    data = {'message': "{} {}".format(request.POST.get('from_user'), ans)}
    return HttpResponse(json.dumps(data), content_type='application/json')

