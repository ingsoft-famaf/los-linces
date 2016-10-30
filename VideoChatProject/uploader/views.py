from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from haystack.management.commands import update_index

from uploader.forms import UploadFileForm
from videochat.models import Video
from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile.image = request.FILES['image']
            request.user.profile.save()

            return render(request, 'upload_image.html', {'alert': 'success'})

        return render(request, 'upload_image.html', {'form': form})
    else:
        form = ImageUploadForm()
        return render(request, 'upload_image.html', {'form': form})


@login_required
def upload(request):
    if request.method == 'POST':
        user = request.user
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_model = Video(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                path=request.FILES['video_file'],
                author=user,
                )
            upload_model.save()
            update_index.Command().handle()

            return render(request, 'upload.html', {'alert': 'success'})
        return render(request, 'upload.html', {'form': form})
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})

@login_required
def delete(request, video_id):
    video = Video.objects.get(pk = video_id)
    #if (user.has_perm('uploader.delete_video'))
    video.delete()
    return render(request, 'delete.html',{'video': video})