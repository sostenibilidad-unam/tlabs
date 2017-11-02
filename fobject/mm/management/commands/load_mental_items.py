from django.core.management.base import BaseCommand
from mm.models import Item, MentalType
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental items from csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='mm types CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:

            item_type = row['TYPE']
            t, created = MentalType.objects.get_or_create(name=item_type)
            if created:
                self.stdout.write("%s: created type %s" % (options['csv'].name, t))
            else:
                self.stdout.write("%s: found type %s" % (options['csv'].name, t))

            item_name = row['ITEM']
            i, created = Item.objects.get_or_create(name=item_name,
                                                    mental_type=t)
            if created:
                self.stdout.write("%s: created item %s" % (options['csv'].name, i))
            else:
                self.stdout.write("%s: found item %s" % (options['csv'].name, i))
