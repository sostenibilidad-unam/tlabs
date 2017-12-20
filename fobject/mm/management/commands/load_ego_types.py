from django.core.management.base import BaseCommand
from mm.models import Alter, Sector
import csv
import argparse


class Command(BaseCommand):
    help = 'Load Ego types from csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='Ego type CSV file')

    def handle(self, *args, **options):
        reader = csv.reader(options['csv'])
        for row in reader:
            ego_name = row[0]
            alter, created = Alter.objects.get_or_create(name=ego_name)
            if created:
                self.stdout.write("%s: created alter %s"
                                  % (options['csv'].name, alter))
            else:
                self.stdout.write("%s: found alter %s"
                                  % (options['csv'].name, alter))

            sector_name = row[1]
            sector, created = Sector.objects.get_or_create(name=sector_name)
            if created:
                self.stdout.write("%s: created sector %s"
                                  % (options['csv'].name, sector))
            else:
                self.stdout.write("%s: found alter %s"
                                  % (options['csv'].name, sector))

            alter.sector = sector
            alter.save()
            self.stdout.write("%s: set sector for %s:%s"
                              % (options['csv'].name, alter, sector))
