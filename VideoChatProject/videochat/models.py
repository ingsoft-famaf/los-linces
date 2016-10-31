from django.db import models
from django.contrib.auth.models import User, Permission

from website import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    path = models.FileField(upload_to="videos/%Y/%m/%d")
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null='True'
    )

    def __str__(self):
        title = 'title: ' + str(self.title)
        description = 'description: ' + str(self.description)
        path = 'path: ' + str(self.path)
        pub_date = 'pub_date: ' + str(self.pub_date)

        return '\n'.join([title, description, path, pub_date])


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    videoHistory = models.ManyToManyField(Video, through='Seen')
    currentlyWatching = models.BooleanField(default=False)
    image = models.ImageField(upload_to="images/%Y/%m/%d", default='images/none/default.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def user_permissions():
    content_type = ContentType.objects.get(app_label='videochat', model='Video')
    permission = Permission.objects.create(codename='delete_video',
                                           name='Can Delete Own Videos',
                                           content_type=content_type)
    permission.save()


class Seen(models.Model):
    video = models.ForeignKey(Video)
    user = models.ForeignKey(Profile)
    started = models.DateTimeField(auto_now_add=True)


