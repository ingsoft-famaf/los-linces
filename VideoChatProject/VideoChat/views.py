from django.shortcuts import render, get_object_or_404
from .models import Video

def play(request, video_id):
	video = get_object_or_404(Video, pk=video_id)
	return render(request, 'reproductor.html', {'video': video})
