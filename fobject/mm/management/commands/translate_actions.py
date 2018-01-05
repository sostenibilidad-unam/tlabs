# coding: utf8
from django.core.management.base import BaseCommand
from mm.models import Action


english = [
    'Capacity building in environmental monitoring',
    'Capacity building in economic analysis',
    'Guided visits',
    'Project management in the delegation',
    'Co-execution of projects',
    'Birds observatory',
    'Strategic collaboration',
    'Chinampas agricultural production',
    'Coordination of guided visits for '
    + 'students (vegetation & chinampas production)',
    'Networking',
    'Assistance in thesis and in chinampa certification studies ',
    'Assistance in developing interviews',
    'Mutual collaboration',
    'Research in water quality',
    'Citizen science project',
    'Capacity building in administrating agricultural projects (for Sn '
    + 'Gregorio producers)',
    'Identify and design the Management Area',
    'Foster collaboration',
    'Complaints and requests',
    'SE BORRA ESTA (pues está medio repetida casi al final): Desarrollo de '
    + 'proyectos sobre construccion de areas verdes y asesoria en '
    + 'mantenimiento corporativo',
    'Assistance in legal framework of urban development in housing',
    'Contact of institutional actors for management',
    'Design and development of image and publicity',
    'Technical assistance on agricultural production',
    'Capacity building in chinampas sustainable use',
    'Financial support',
    'Develop projects for construction and maintenance of green areas ',
    'Exchange of information ',
    'Assistance in ecological information',
    'Fauna refugees and ecological restoration',
    'Sale of agricultural products']


class Command(BaseCommand):
    help = 'Rename actions with in_degree>1 to included english translations.'

    def handle(self, *args, **options):
        for a in Action.objects.order_by("in_degree").filter(in_degree__gt=1):
            translation = english.pop(0)
            print a.action, translation
            a.action = translation
            a.save()
