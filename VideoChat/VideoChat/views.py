from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from VideoChat.forms import UploadFileForm
from VideoChat.models import Video

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['video_file'])
            #return HttpResponseRedirect('/success/url/')
            return render(request, 'upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('writefile', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
