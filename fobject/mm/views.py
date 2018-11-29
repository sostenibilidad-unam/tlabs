from __future__ import unicode_literals
import json
from .models import Alter, Phase, AgencyNetwork, Action, \
    MentalModel, PowerNetwork
from django.shortcuts import render, redirect
from django.views import View

from django.http import HttpResponse


def index(request):
    context = {'phases': Phase.objects.all(),
               'title': 'T-Labs',
               'egos': Alter.objects.filter(name__startswith="TL0").all()}

    return render(request, 'index.html', context)


def power_json(request):
    g = PowerNetwork(ego_ids=request.session['ego_ids'],
                     phase_id=request.session['phase_id'])
    return HttpResponse(json.dumps(g.get_json()))


def ana_json(request):
    g = AgencyNetwork(ego_ids=request.session['ego_ids'],
                      phase_id=request.session['phase_id'])
    return HttpResponse(json.dumps(g.get_json()))


def view_alter(request, alter_id):
    request.session['ego_ids'] = [int(alter_id), ]
    return redirect('ana_view')


def view_action(request, action_id):
    phase = Phase.objects.get(pk=request.session['phase_id'])
    action = Action.objects.get(pk=action_id)
    request.session['ego_ids'] = [e.alter.id
                                  for e in
                                  action.actor_set.filter(phase=phase)]
    return redirect('ana_view')


def mm_json(request):
    mm = MentalModel(ego_ids=request.session['ego_ids'],
                     phase_id=request.session['phase_id'])
    return HttpResponse(json.dumps(mm.get_compound_json()))


class MMView(View):

    template = 'mm.html'

    def get(self, request, *args, **kwargs):
        context = {'ego_ids': request.session['ego_ids'],
                   'title': ", ".join(
                       [Alter.objects.get(pk=eid).name
                        for eid in request.session['ego_ids']])}
        return render(request,
                      self.template,
                      context)


class Ana(View):

    template = 'ana.html'

    def get(self, request, *args, **kwargs):
        context = {'ego_ids': request.session['ego_ids'],
                   'layout': kwargs['layout'],
                   'title': ", ".join(
                       [Alter.objects.get(pk=eid).name
                        for eid in request.session['ego_ids']])}
        return render(request,
                      self.template,
                      context)


class Power(View):

    template = 'power.html'

    def get(self, request, *args, **kwargs):
        context = {'ego_ids': request.session['ego_ids'],
                   'title': ", ".join(
                       [Alter.objects.get(pk=eid).name
                        for eid in request.session['ego_ids']])}
        return render(request,
                      self.template,
                      context)


class AnaSetup(View):

    template = 'ana_setup.html'

    context = {'phases': Phase.objects.all(),
               'title': 'T-Labs',
               'egos': Alter.objects.filter(name__startswith="TL0").all()}

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template,
                      self.context)

    def post(self, request, *args, **kwargs):
        ego_ids = []
        for key in request.POST:
            if 'ego' in key:
                k, ego_id = key.split('_')
                ego_ids.append(int(ego_id))

        request.session['ego_ids'] = ego_ids
        request.session['phase_id'] = request.POST['phase']

        if request.POST['next'] == 'Agency Network Dagre':
            return redirect('ana_view', layout='dagre')
        elif request.POST['next'] == 'Agency Network Cose':
            return redirect('ana_view', layout='cose')            
        elif request.POST['next'] == 'Mental Model':
            return redirect('mm_view')
        elif request.POST['next'] == 'Power Network':
            return redirect('power_view')
