from django.shortcuts import render
from Base.models import Video

def play(request, video_id):
	return render(request, 'reproductor.html')
