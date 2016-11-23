from django.db import models
from django.contrib.auth.models import User, Permission

from django.utils.dateformat import format
from website import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import time

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    path = models.FileField(upload_to="videos")
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null='True'
    )
    thumbnail = models.ImageField(default="images/none/default_thumbnail.jpg")

    def __str__(self):
        title = 'title: ' + str(self.title)
        description = 'description: ' + str(self.description)
        path = 'path: ' + str(self.path)
        pub_date = 'pub_date: ' + str(self.pub_date)

        return '\n'.join([title, description, path, pub_date])

    def is_watched_by(self, user):
        user.profile.currentlyWatching = True
        user.profile.save()
        seen = Seen.objects.create(video=self, user=user.profile)
        seen.save()


class Chatroom(models.Model):
    users = models.ManyToManyField(User)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        )

    def last_message(self):
        last = self.messages.last()
        if last is not None:
            return last.pk
        else:
            return -1

    def add_play_event(self):
        event_type, relative_time = \
            self.get_last_event_type_and_time()

        if event_type != Event.PLAY_STATE:
            event = Event.objects.create(
                    event_type = Event.PLAY_STATE,
                    relative_time = relative_time,
                    chatroom = self,
                    )

    def add_pause_event(self):
        event_type, relative_time = \
            self.get_last_event_type_and_time()

        if event_type != Event.PAUSE_STATE:
            event = Event.objects.create(
                    event_type = Event.PAUSE_STATE,
                    relative_time = relative_time,
                    chatroom = self,
                    )

    def add_change_video_event(self, new_video_src):
        event = Event.objects.create(
            event_type = Event.CHANGE_VIDEO_STATE,
            relative_time = 0,
            chatroom = self,
            video_src = new_video_src,
            )

    def get_last_event_type_and_time(self):
        last_event = Event.objects.filter(chatroom=self).last()

        event_type = None
        relative_time = 0
        if last_event != None:
            event_type = last_event.event_type
            if event_type == Event.PLAY_STATE:
                relative_time = last_event.relative_time + (int(time.time()) - int(format(last_event.time, 'U')))
            elif event_type == Event.PAUSE_STATE:
                relative_time = last_event.relative_time

        return event_type, relative_time


class Event(models.Model):
    PLAY_STATE = 0
    PAUSE_STATE = 1
    CHANGE_VIDEO_STATE = 2

    event_type = models.IntegerField(default=PLAY_STATE)
    time = models.DateTimeField(auto_now=True)
    relative_time = models.IntegerField()
    chatroom = models.ForeignKey(
        Chatroom,
        on_delete=models.CASCADE,
        )
    video_src = models.CharField(max_length=200, default=None)

class Message(models.Model):
    text = models.TextField()
    date_sent = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null='True'
    )
    chatroom = models.ForeignKey(
        Chatroom,
        on_delete=models.CASCADE,
        related_name="messages")


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    videoHistory = models.ManyToManyField(Video, through='Seen')
    currentlyWatching = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images", default='images/none/default_profile.png')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Seen(models.Model):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(Profile)
    started = models.DateTimeField(auto_now_add=True)
