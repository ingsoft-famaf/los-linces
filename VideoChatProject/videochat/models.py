from django.db import models
from django.contrib.auth.models import User, Permission

from website import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Chatroom(models.Model):
    PLAY_STATE = 0
    PAUSE_STATE = 1

    state = models.CharField(max_length=20)
    users = models.ManyToManyField(User)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        )


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
        on_delete=models.CASCADE)


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
