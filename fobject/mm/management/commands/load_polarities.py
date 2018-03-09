from django.core.management.base import BaseCommand
from mm.models import Alter, Phase, EgoEdge
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('--phase', help='Phase name', required=True)

        parser.add_argument('--csv', type=argparse.FileType('r'),
                            required=True,
                            help='mm CSV file')

    def handle(self, *args, **options):
        phase = Phase.objects.get(phase=options['phase'])
        reader = csv.reader(options['csv'])
        for row in reader:

            try:
                source_name = row[0]
                s = Alter.objects.get(name=source_name)

                target_name = row[1]
                t = Alter.objects.get(name=target_name)

                e = EgoEdge.objects.get(source=s, target=t, phase=phase)
                e.polarity = row[2]

                print e
                e.save()
            except:
                pass
