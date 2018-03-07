from django.core.management.base import BaseCommand
from mm.models import Variable, MentalEdge, Alter, Phase
import csv
import argparse


class Command(BaseCommand):
    help = 'Load mental edges from csv edgelist'

    def add_arguments(self, parser):
        parser.add_argument('--ego', help='Ego name', required=True)

        parser.add_argument('--phase', help='Phase name', required=True)

        parser.add_argument('--csv', type=argparse.FileType('r'),
                            required=True,
                            help='mm CSV file')

    def handle(self, *args, **options):
        reader = csv.DictReader(options['csv'])
        for row in reader:
            phase = Phase.objects.get(phase=options['phase'])
            e = Alter.objects.get(name=options['ego'])

            source_name = row['SOURCE']
            s = Variable.objects.get(name=source_name)

            target_name = row['TARGET']
            t = Variable.objects.get(name=target_name)

            e = MentalEdge(source=s, target=t, ego=e, phase=phase)
            e.save()

            self.stdout.write("%s: created edge %s" % (options['csv'].name, e))
