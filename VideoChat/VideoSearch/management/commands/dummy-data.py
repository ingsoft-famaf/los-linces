from model_mommy import mommy
from django.core.management.base import BaseCommand
from . import markovgen
import os
from Base.models import Video


class Command(BaseCommand):
    help = "My shiny new management command."
    videos = []

    def add_arguments(self, parser):
        parser.add_argument('count', nargs=1, type=int)

    def handle(self, *args, **options):
        print("Hi")
        self.clear()
        self.make_videos(options)

    def make_videos(self, options):
        f = open(os.path.abspath("VideoSearch/management/commands/source"))
        markov = markovgen.Markov(f)
        for _ in range(options.get('count')[0]):
            video_title = markov.generate_markov_text(10)
            video_description = markov.generate_markov_text(200)
            video = mommy.make(Video, title=video_title, description=video_description)

            self.videos.append(video)

    def clear(self):
        Video.objects.all().delete()