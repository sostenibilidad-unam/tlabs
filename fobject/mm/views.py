# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from .models import Alter, ActionEdge
from django.shortcuts import render

from django.http import HttpResponse

import networkx as nx


def sector_color(alter):
    sector_color = {'Academia': 'blue',
                    'Gobierno': 'green',
                    None: 'orange',
                    'Ego': 'red',
                    'Otros': 'purple',
                    'Privado': 'purple',
                    'Sociedad_Civil': 'gold'}
    if alter.sector:
        sector = alter.sector.name
    else:
        sector = None

    return sector_color[sector]


def practice_color(action):
    practice_color = {
        'Research': 'darkcyan',
        'Training': 'firebrick',
        'Agricultural/ecological training': 'orange',
        'Outreach': 'green',
        'Market': 'blue',
        'Education': 'teal',
        'Funding': 'grey',
        'Collaboration': 'red',
        'Financial/commercial training': 'yellow',
        'Social organization': 'cornflowerblue',
        'Tourism': 'forestgreen',
        'Management': 'dodgerblue',
        'Networking': 'goldenrod',
        'Production': 'midnightblue',
        'Construction': 'darkgreen',
        'Culture': 'cyan',
        'Consultancy': 'hotpink',
        'Ecological conservation': 'lightcoral',
        'Citizen assistance': 'indigo',
        'Legal training': 'brown',
    }
    if action.category:
        return practice_color[action.category.name]
    else:
        return "purple"


def ego_net_json(request, ego_id):
    ego = Alter.objects.get(id=ego_id)

    g = nx.Graph()

    # create network from egos to alters
    for e in ego.ego_net.all():
        if e.source.name.startswith('TL0'):
            g.add_node(e.source.id,
                       name=e.source.name,
                       shape="triangle",
                       scolor=sector_color(e.source))
        else:
            g.add_node(e.source.id,
                       name=e.source.name,
                       shape="ellipse",
                       scolor=sector_color(e.source))
            for action_e in ActionEdge.objects.filter(alter=e.source):
                g.add_node(action_e.action.action,
                           name=action_e.action.action,
                           shape='rectangle',
                           scolor=practice_color(action_e.action))
                g.add_edge(action_e.alter.id,
                           action_e.action.action)

        if e.target.name.startswith('TL0'):
            g.add_node(e.target.id,
                       name=e.target.name,
                       shape="triangle",
                       scolor=sector_color(e.target))
        else:
            g.add_node(e.target.id,
                       name=e.target.name,
                       shape="ellipse",
                       scolor=sector_color(e.target))
            for action_e in ActionEdge.objects.filter(alter=e.target):
                g.add_node(action_e.action.action,
                           name=action_e.action.action,
                           shape='rectangle',
                           scolor=practice_color(action_e.action))
                g.add_edge(action_e.alter.id,
                           action_e.action.action)

        g.add_edge(e.source.id,
                   e.target.id,
                   distance=e.distance,
                   interaction=e.interaction)

    net = {'nodes': [{'data': {'id': n,
                               'href': '/ego/%s/' % n,
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
