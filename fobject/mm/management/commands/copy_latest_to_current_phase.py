from django.core.management.base import BaseCommand
from mm.models import EgoEdge, ActionEdge, MentalEdge, PowerEdge, \
    Phase, Alter, Action, Variable, Power


class Command(BaseCommand):
    help = 'Update networks copying from latest available to specified phase'

    def add_arguments(self, parser):
        parser.add_argument('target',
                            help='target phase name')

    def handle(self, *args, **options):

        target = Phase.objects.get(phase=options['target'])

        # copy ego edge
        print "copying ego edges"
        for s in Alter.objects.all():
            for t in Alter.objects.all():
                if EgoEdge.objects.filter(
                        source=s,
                        target=t).exclude(phase=target).count() > 0:
                    ee = EgoEdge.objects.filter(
                        source=s,
                        target=t
                    ).exclude(phase=target).last()
                    ee.pk = None
                    ee.phase = target
                    ee.save()

        # copy action edges
        print "copying action edges"
        for s in Alter.objects.all():
            for t in Action.objects.all():
                if ActionEdge.objects.filter(
                        alter=s,
                        action=t).exclude(phase=target).count() > 0:
                    ae = ActionEdge.objects.filter(
                        alter=s,
                        action=t
                    ).exclude(phase=target).last()
                    ae.pk = None
                    ae.phase = target
                    ae.save()

        # copy mental model
        print "copy mental model"
        for ego in Alter.objects.all():
            for s in Variable.objects.all():
                for t in Variable.objects.all():
                    if MentalEdge.objects.filter(
                            source=s,
                            target=t,
                            ego=ego
                    ).exclude(phase=target).count() > 0:
                        me = MentalEdge.objects.filter(
                            source=s,
                            target=t,
                            ego=ego
                        ).exclude(phase=target).last()
                        me.pk = None
                        me.phase = target
                        me.save()

        # copy power edges
        print "copying power edges"
        for s in Alter.objects.all():
            for t in Power.objects.all():
                if PowerEdge.objects.filter(
                        source=s,
                        target=t).exclude(phase=target).count() > 0:
                    pe = PowerEdge.objects.filter(
                        source=s,
                        target=t
                    ).exclude(phase=target).last()
                    pe.pk = None
                    pe.phase = target
                    pe.save()
