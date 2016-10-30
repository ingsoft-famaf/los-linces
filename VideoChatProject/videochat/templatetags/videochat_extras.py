from django.template import Library
from django.contrib.auth.models import User
from friendship.models import Friend
from friendship.models import FriendshipRequest

register = Library()


@register.filter
def get_tuples(value, arg):
    lst = value
    size = arg
    res = []
    while lst:
        sl = lst[:size]
        res.append(tuple(sl))
        lst = lst[size:]
    return res


@register.filter
def check_not_friends(value, arg):
    current_user_pk = value
    other_user_pk = arg

    current_user = User.objects.get(pk=current_user_pk)
    other_user = User.objects.get(pk=other_user_pk)

    return other_user not in Friend.objects.friends(current_user)


@register.filter
def check_request_sent(value, arg):
    current_user_pk = value
    other_user_pk = arg

    current_user = User.objects.get(pk=current_user_pk)
    other_user = User.objects.get(pk=other_user_pk)

    return FriendshipRequest.objects.filter(from_user=current_user, to_user=other_user)
