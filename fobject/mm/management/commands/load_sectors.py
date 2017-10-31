from django.core.management.base import BaseCommand, CommandError
from mm.models import Alter
import argparse

class Command(BaseCommand):
    help = 'Load alters from csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'))

    def handle(self, *args, **options):
        for alter_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
