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
            source_name = row['SOURCE']
            alter, created = Alter.objects.get_or_create(name=source_name)
            if created:
                self.stdout.write("%s: created alter %s" % (options['csv'].name, alter))
            else:
                self.stdout.write("%s: found alter %s" % (options['csv'].name, alter))

            target_name = row['TARGET']
            action, created = Action.objects.get_or_create(action=target_name.encode('utf-8'))
            if created:
                self.stdout.write(u"%s: created action %s" % (options['csv'].name, action))
            else:
                self.stdout.write(u"%s: found action %s" % (options['csv'].name, action))

            e, created = Agency.objects.get_or_create(alter=alter,
                                                      action=action)
            if created:
                self.stdout.write(u"%s: created agency %s" % (options['csv'].name, e))
            else:
                self.stdout.write(u"%s: found agency %s" % (options['csv'].name, e))
