from model_mommy import mommy
from django.core.management.base import BaseCommand
from . import markovgen
import os
from haystack.management.commands import update_index
from videochat.models import Video


class Command(BaseCommand):
    videos = []

    def add_arguments(self, parser):
        parser.add_argument('action', nargs=1, type=str)
        parser.add_argument('count', nargs=1, type=int)

    def handle(self, *args, **options):
        if options.get('action')[0] == 'create':
            print("Creating dummy data...")
            self.make_videos(options)
            update_index.Command().handle()

        if options.get('action')[0] == 'clear':
            print("Deleting dummy data...")
            self.clear()

        if options.get('action')[0] == 'count':
            self.count()

    def make_videos(self, options):
        f = open(os.path.abspath("videochat/management/commands/source"))
        markov = markovgen.Markov(f)
        for i in range(options.get('count')[0]):
            # video_title = markov.generate_markov_text(10)
            video_title = "sample " + str(i)
            video_description = markov.generate_markov_text(100)
            video = mommy.make(Video, title=video_title, description=video_description)

            self.videos.append(video)

    def clear(self):
        Video.objects.all().delete()

    def count(self):
        print("Count: " + str(Video.objects.all().count()))
