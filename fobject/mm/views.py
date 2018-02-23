# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .models import Alter
from django.shortcuts import render

from django.http import HttpResponse

import networkx as nx


def sector_color(alter):
    sector_color = {'Academia': 'blue',
                    'Gobierno': 'green',
                    None: 'orange',
                    'Otros': 'purple',
                    'Privado': 'purple',
                    'Sociedad_Civil': 'yellow'}
    if alter.sector:
        sector = alter.sector.name
    else:
        sector = None

    return sector_color[sector]


def ego_net_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)

    g = nx.Graph()

    for e in ego.ego_net.all():
        if e.source.name.startswith('TL0'):
            source_shape = "triangle"
        else:
            source_shape = "ellipse"
        g.add_node(e.source.id,
                   name=e.source.name,
                   shape=source_shape,
                   scolor=sector_color(e.source))

        if e.target.name.startswith('TL0'):
            target_shape = "triangle"
        else:
            target_shape = "ellipse"
        g.add_node(e.target.id,
                   name=e.target.name,
                   shape=target_shape,
                   scolor=sector_color(e.target))

        g.add_edge(e.source.id,
                   e.target.id,
                   distance=e.distance,
                   interaction=e.interaction)

    net = {'nodes': [{'data': {'id': n,
                               'name': g.node[n]['name'],
                               'shape': g.node[n]['shape'],
                               'scolor': g.node[n]['scolor']}}
                     for n in g.nodes],
           'edges': [{'data': {'source': e[0],
                               'target': e[1]}} for e in g.edges]}

    return HttpResponse(json.dumps(net))


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
               'egos': Alter.objects.filter(name__startswith="TL0").all()}
    return render(request, 'ego_net_cy.html', context)


def mm(request, ego_id):
    ego = Alter.objects.get(id=ego_id)
    context = {'ego': ego,
               'egos': Alter.objects.filter(name__startswith="TL0").all()}
    return render(request, 'mm.html', context)


def mm_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)
    return HttpResponse(ego.mental_model())
