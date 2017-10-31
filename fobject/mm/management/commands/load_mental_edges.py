from django.core.management.base import BaseCommand
from mm.models import Item, MentalEdge, Alter
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('--ego', help='Ego string')

        parser.add_argument('--csv', type=argparse.FileType('r'),
                            help='mm CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            e = Alter.objects.get(name=options['ego'])

            source_name = row['SOURCE']
            s, created = Item.objects.get_or_create(name=source_name)
            if created:
                self.stdout.write("created item %s" % s)
            else:
                self.stdout.write("found item %s" % s)

            target_name = row['TARGET']
            t, created = Item.objects.get_or_create(name=target_name)
            if created:
                self.stdout.write("created item %s" % t)
            else:
                self.stdout.write("found item %s" % t)

            e = MentalEdge(source=s, target=t, ego=e)
            e.save()

            self.stdout.write("loaded edge %s" % e)
