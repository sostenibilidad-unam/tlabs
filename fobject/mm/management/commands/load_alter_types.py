from django.core.management.base import BaseCommand
from mm.models import Type, Alter
import csv
import argparse


class Command(BaseCommand):
    help = 'Load alter types from csv'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='agencynet type CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:

            alter_name = row['SOURCE']
            a = Alter.objects.get(name=alter_name)

            type_name = row['TARGET']
            t, created = Type.objects.get_or_create(name=type_name)
            if created:
                self.stdout.write("created type %s" % t)
            else:
                self.stdout.write("found type %s" % t)

            a.type = t
            a.save()
