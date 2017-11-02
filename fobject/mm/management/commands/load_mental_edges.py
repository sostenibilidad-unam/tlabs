from django.core.management.base import BaseCommand
from mm.models import Item, MentalEdge, Alter
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('--ego', help='Ego string', required=True)

        parser.add_argument('--csv', type=argparse.FileType('r'),
                            required=True,
                            help='mm CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            e = Alter.objects.get(name=options['ego'])

            source_name = row['SOURCE']
            s, created = Item.objects.get_or_create(name=source_name)
            if created:
                self.stdout.write("%s: created item %s" % (options['csv'].name, s))
            else:
                self.stdout.write("%s: found item %s" % (options['csv'].name, s))

            target_name = row['TARGET']
            t, created = Item.objects.get_or_create(name=target_name)
            if created:
                self.stdout.write("%s: created item %s" % (options['csv'].name, t))
            else:
                self.stdout.write("%s: found item %s" % (options['csv'].name, t))

            e = MentalEdge(source=s, target=t, ego=e)
            e.save()

            self.stdout.write("%s: created edge %s" % (options['csv'].name, e))
