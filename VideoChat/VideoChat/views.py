from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from VideoChat.forms import UploadFileForm
from VideoChat.models import Video

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
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
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

