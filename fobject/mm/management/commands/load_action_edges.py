from django.core.management.base import BaseCommand
from mm.models import Alter, Agency, Action
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='agency CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            try:
                source_name = row['SOURCE']
                alter = Alter.objects.get(name=source_name)
            except:
                self.stderr.write("NO ENCONTRAR %s" % source_name)

            target_name = row['TARGET']
            action, created = Action.objects.get_or_create(action=target_name)
            if created:
                self.stdout.write("created action %s" % action)
            else:
                self.stdout.write("found action %s" % action)

            e, created = Agency.objects.get_or_create(alter=alter,
                                                      action=action)
            if created:
                self.stdout.write("created agency %s" % e)
            else:
                self.stdout.write("found agency %s" % e)
