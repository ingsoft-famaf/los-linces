from django.contrib.auth import authenticate, logout, \
                                update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404

from haystack.management.commands import update_index
from videochat.models import Seen, Video, Chatroom
from friendship.models import Friend

from .forms import ProfileForm

@login_required
def index(request):
    videos_being_watched = []
    for friend in Friend.objects.friends(request.user):
        try:
            if friend.profile.currentlyWatching:
                video = Seen.objects.filter(user__user=friend).order_by('-id').first().video
                chatroom = Chatroom.objects.filter(video=video, users__in=[friend]).last()
                videos_being_watched.append((friend, video, chatroom))
        except IndexError:
            continue

    return render(request, 'index.html', {'videos_being_watched': videos_being_watched})


def register_view(request):
    if request.POST:
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            update_index.Command().handle()
            new_profile = profile_form.save()
            return redirect('/')
        else:
            return render(request, 'register.html', {'user_form': user_form, 
                                                    'profile_form': profile_form})

    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'register.html', {'user_form': user_form, 
                                                'profile_form': profile_form})


def login_view(request):
    if request.POST:
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('/')
        else:
            errors = ["Invalid username or password"]
            return render(request, 'login.html', {'form': form, 'errors': errors})

    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

'''
def logout_view(request):
    logout(request)
    return redirect('/')
'''
