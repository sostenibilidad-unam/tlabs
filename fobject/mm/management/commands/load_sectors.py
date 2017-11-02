from django.core.management.base import BaseCommand
from mm.models import Sector, Alter
import csv
import argparse


class Command(BaseCommand):
    help = 'Load alters from csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='egonet_type CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            sector_name = row['TYPE']
            s, created = Sector.objects.get_or_create(name=sector_name)
            if created:
                self.stdout.write("%s: created sector %s" % (options['csv'].name, s))
            else:
                self.stdout.write("%s: found sector %s" % (options['csv'].name, s))

            alter_name = row['ITEM']
            a, created = Alter.objects.get_or_create(name=alter_name, sector=s)
            if created:
                self.stdout.write("%s: created alter %s" % (options['csv'].name, a))
            else:
                self.stdout.write("%s: found alter %s" % (options['csv'].name, a))
