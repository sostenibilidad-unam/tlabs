from __future__ import print_function
from django.core.management.base import BaseCommand
from mm.models import EgoEdge, ActionEdge, MentalEdge, PowerEdge, Phase


class Command(BaseCommand):
    help = 'Copy networks from one phase to another'

    def add_arguments(self, parser):
        parser.add_argument('phase0',
                            help='source phase name')
        parser.add_argument('phase1',
                            help='target phase name')

    def handle(self, *args, **options):

        phase0 = Phase.objects.get(phase=options['phase0'])
        phase1 = Phase.objects.get(phase=options['phase1'])

        # copy ego edge
        print("copying ego edges")
        for edge in EgoEdge.objects.filter(phase=phase0):
            edge.pk = None
            edge.phase = phase1
            edge.save()
            print(".", end='')

        # copy action edges
        print("\ncopying action edges")
        for action_edge in ActionEdge.objects.filter(phase=phase0):
            action_edge.pk = None
            action_edge.phase = phase1
            action_edge.save()
            print(".", end='')

        # copy mental model
        print("\ncopying mental edges")
        for mental_edge in MentalEdge.objects.filter(phase=phase0):
            mental_edge.pk = None
            mental_edge.phase = phase1
            mental_edge.save()
            print(".", end='')

        # copy power edges
        print("\ncopying power edges")
        for power_edge in PowerEdge.objects.filter(phase=phase0):
            power_edge.pk = None
            power_edge.phase = phase1
            power_edge.save()
            print(".", end='')

        print()
