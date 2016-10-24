from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from haystack.management.commands import update_index

from uploader.forms import UploadFileForm
from videochat.models import Video


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
            #update_index.Command().handle()
            return HttpResponseRedirect('/success/upload')
        return render(request, 'upload.html', {'form': form})

    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
