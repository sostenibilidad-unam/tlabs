# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .models import Alter
from django.shortcuts import render

from django.http import HttpResponse

import networkx as nx


def ego_net_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)

    g = nx.Graph()

    for e in ego.ego_net.all():
        g.add_edge(e.source.name,
                   e.target.name,
                   distance=e.distance,
                   interaction=e.interaction)

    return HttpResponse(json.dumps(nx.node_link_data(g), indent=2))


def mm_net_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)

    g = nx.Graph()

    for e in ego.ego_net.all():
        g.add_edge(e.source.name,
                   e.target.name,
                   distance=e.distance,
                   interaction=e.interaction)

    return HttpResponse(json.dumps(nx.node_link_data(g), indent=2))


def ego_nets(request, ego_id):
    ego = Alter.objects.get(id=ego_id)
    context = {'ego': ego,
               'alters': Alter.objects.all()}
    return render(request, 'ego_net.html', context)
