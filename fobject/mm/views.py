from __future__ import unicode_literals
import json
from .models import Alter, Phase, AgencyNetwork, Action
from django.shortcuts import render, redirect
from django.views import View

from django.http import HttpResponse

import networkx as nx


def index(request):
    context = {'phases': Phase.objects.all(),
               'title': 'T-Labs',
               'egos': Alter.objects.filter(name__startswith="TL0").all()}

    return render(request, 'index.html', context)


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


class Ana(View):

    template = 'ana.html'

    def get(self, request, *args, **kwargs):
        context = {'ego_ids': request.session['ego_ids']}
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
        return redirect('ana_view')


def mm_net_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)

    g = nx.Graph()

    for e in ego.ego_net.all():
        g.add_edge(e.source.name,
                   e.target.name,
                   distance=e.distance,
                   interaction=e.interaction)

    return HttpResponse(json.dumps(nx.node_link_data(g), indent=2))


def mm(request, ego_id):
    ego = Alter.objects.get(id=ego_id)
    context = {'ego': ego,
               'egos': Alter.objects.filter(name__startswith="TL0").all()}
    return render(request, 'mm.html', context)


def mm_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)
    return HttpResponse(ego.mental_model())
