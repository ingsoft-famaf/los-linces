from haystack.management.commands import update_index
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from uploader.forms import UploadFileForm
from videochat.models import Video


def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_model = Video(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                path=request.FILES['video_file'],
                )
            upload_model.save()
            #update_index.Command().handle()
            return HttpResponseRedirect('/success/upload')
        return render(request, 'upload.html', {'form': form})

    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
