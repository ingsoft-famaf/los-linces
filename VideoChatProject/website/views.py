from django.contrib.auth import authenticate, logout, \
                                update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from haystack.management.commands import update_index
from videochat.models import Seen, Video
from friendship.models import Friend


@login_required
def index(request):
    videos_being_watched = []
    for friend in Friend.objects.friends(request.user):
        try:
            if friend.profile.currentlyWatching:
                videos_being_watched.append((friend, Seen.objects.filter(user__user=friend).order_by('-id')[0].video))
        except IndexError:
            continue

    return render(request, 'index.html', {'videos_being_watched': videos_being_watched})


def register_view(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            update_index.Command().handle()
            return redirect('/')
        else:
            return render(request, 'register.html', {'form': form})

    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})


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
