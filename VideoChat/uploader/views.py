from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from uploader.forms import UploadFileForm
from uploader.models import Video

import magic

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if checkfile(request.FILES['video_file'].read(1024)):
                upload_model = Video(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    path=request.FILES['video_file'],
                    duration=2.5,
                    )
                upload_model.save()

                # should redirect to "upload/success"
                return render(request, 'upload.html', {'form': form})
            else:
                # bad file format
                pass
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def check_file_format(read_data):
    pass
