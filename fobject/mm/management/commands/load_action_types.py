from django.core.management.base import BaseCommand
from mm.models import Action, Category
import csv
import argparse


class Command(BaseCommand):
    help = 'Load action categories'

    def add_arguments(self, parser):
        parser.add_argument('csv', type=argparse.FileType('r'),
                            help='action categories CSV file')

    def handle(self, *args, **options):
        reader = csv.reader(options['csv'], delimiter=":")
        for row in reader:
            cat_name = row[1]
            cat, created = Category.objects.get_or_create(name=cat_name)
            if created:
                self.stdout.write(u"%s: created category %s"
                                  % (options['csv'].name, cat))
            else:
                self.stdout.write(u"%s: found category %s"
                                  % (options['csv'].name, cat))

            action_name = row[0]
            action, created = Action.objects.get_or_create(
                action=action_name.decode('utf-8'))
            if created:
                self.stdout.write(u"%s: created action %s"
                                  % (options['csv'].name, action))
            else:
                self.stdout.write(u"%s: found action %s"
                                  % (options['csv'].name, action))
            action.category = cat
            action.save()
