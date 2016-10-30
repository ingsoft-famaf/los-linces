from friendship.models import Friend
import json
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from friendship.models import FriendshipRequest


@csrf_exempt
def finish_watching(request):
    if request.is_ajax() and request.POST:
        current_user = User.objects.get(pk=request.POST.get('user'))

        current_user.profile.currentlyWatching = False
        current_user.profile.save()
        data = {'message': "{} finished watching a video".format(request.POST.get('user'))}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def add_friend(request):
    if request.is_ajax() and request.POST:
        from_user = User.objects.get(pk=request.POST.get('from_user'))
        to_user = User.objects.get(pk=request.POST.get('to_user'))

        Friend.objects.add_friend(from_user, to_user)
        data = {'message': "{} added".format(request.POST.get('to_user'))}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def cancel_fr(request):
    if request.is_ajax() and request.POST:
        from_user = User.objects.get(pk=request.POST.get('from_user'))
        to_user = User.objects.get(pk=request.POST.get('to_user'))

        FriendshipRequest.objects.get(from_user=from_user, to_user=to_user).delete()
        data = {'message': "{} friendship request deleted".format(request.POST.get('to_user'))}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def handle_request(request):
        if request.is_ajax() and request.POST:

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
        else:
            raise Http404

