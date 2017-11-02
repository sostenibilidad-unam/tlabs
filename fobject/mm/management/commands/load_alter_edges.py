from django.core.management.base import BaseCommand
from mm.models import Alter, EgoEdge
import csv
import argparse


class Command(BaseCommand):
    help = 'Load alter edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='egonet CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            # SOURCE,TARGET,INTERACTION,DISTANCE

            source_name = row['SOURCE']
            s, created = Alter.objects.get_or_create(name=source_name)
            if created:
                self.stdout.write("%s: created alter %s" % (options['csv'].name, s))
            else:
                self.stdout.write("%s: found alter %s" % (options['csv'].name, s))

            target_name = row['TARGET']
            t, created = Alter.objects.get_or_create(name=target_name)
            if created:
                self.stdout.write("%s: created alter %s" % (options['csv'].name, t))
            else:
                self.stdout.write("%s: found alter %s" % (options['csv'].name, t))

            e = EgoEdge(source=s, target=t,
                        interaction=row['INTERACTION'],
                        distance=int(row['DISTANCE']))
            e.save()
