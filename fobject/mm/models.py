# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import networkx as nx
import colors
from django.conf import settings
from django.db import models


class Phase(models.Model):
    phase = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.phase


class Sector(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class Power(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class Alter(models.Model):
    name = models.CharField(max_length=200)
    sector = models.ForeignKey(Sector, null=True)
    desc = models.TextField(blank=True)

    degree = models.IntegerField(default=0)

    avatar_name = models.CharField(max_length=200, blank=True)
    avatar_pic = models.ImageField(blank=True, null=True,
                                   upload_to='avatars/')

    def mental_model(self, phase):
        g = nx.DiGraph()

        for e in self.mentaledge_set.filter(phase=phase):
            g.add_node(e.source.name,
                       shape="ellipse"
                       if "Proceso" in e.source.mental_type
                       else "rectangle")

            g.add_node(e.target.name,
                       shape="ellipse"
                       if "Proceso" in e.target.mental_type
                       else "rectangle")

            g.add_edge(e.source.name,
                       e.target.name)
        return g

    def compound_mental_model(self, phase):
        g = nx.DiGraph()

        for e in self.mentaledge_set.filter(phase=phase):
            g.add_node(e.source.name, egos=[])

            g.add_node(e.target.name, egos=[])

            g.add_edge(e.source.name,
                       e.target.name)
        return g

    def power_network(self, phase):
        g = nx.Graph()

        for e in self.powers.filter(phase=phase):
            g.add_node(e.source.name,
                       shape="ellipse",
                       width=120,
                       height=120,
                       avatar=e.source.avatar_url())
            g.add_node(e.target.name,
                       shape="octagon",
                       width=90,
                       height=90)

            g.add_edge(e.source.name,
                       e.target.name)
        return g

    def avatar_url(self):
        if self.avatar_pic:
            return u"%s%s" % (settings.MEDIA_URL, self.avatar_pic)
        else:
            return None

    def image_tag(self):
        if self.avatar_pic:
            return u'<img src="/media/%s" width="40px"/>' % self.avatar_pic
        else:
            return u'&nbsp;'

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name_plural = "Egos and Alters"


class EgoEdge(models.Model):
    source = models.ForeignKey(Alter, related_name='ego_net')
    target = models.ForeignKey(Alter, related_name='alter_for')

    distance = models.IntegerField()

    interaction = models.CharField(max_length=20)

    polarity = models.IntegerField(default=0)

    influence_source = models.IntegerField(default=0)
    influence_target = models.IntegerField(default=0)

    phase = models.ForeignKey(Phase, null=True)

    def __unicode__(self):
        return u"%s<-%s->%s" % (self.source, self.distance, self.target)


class PowerEdge(models.Model):
    source = models.ForeignKey(Alter, related_name='powers')
    target = models.ForeignKey(Power, related_name='wielded_by')

    phase = models.ForeignKey(Phase, null=True)

    def __unicode__(self):
        return u"%s -- %s" % (self.source, self.target)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def alters(self):
        return [a for a in self.action_set.all()]

    def get_degree(self):
        return sum([a.in_degree for a in self.alters()])

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return u"%s" % self.name


class Action(models.Model):
    action = models.CharField(max_length=200)
    category = models.ForeignKey(Category, null=True)

    in_degree = models.IntegerField(default=0)

    def update_in_degree(self, phase):
        self.in_degree = self.actor_set.filter(phase=phase).count()

    def __unicode__(self):
        return u"%s" % self.action


class ActionEdge(models.Model):
    alter = models.ForeignKey(Alter,
                              related_name='action_set',
                              null=True)
    action = models.ForeignKey(Action,
                               related_name='actor_set',
                               null=True)

    phase = models.ForeignKey(Phase, null=True)

    class Meta:
        verbose_name_plural = "Action Edges"

    def __unicode__(self):
        return u"%s->%s" % (self.alter, self.action)


class Variable(models.Model):
    name = models.CharField(max_length=200)
    mental_type = models.CharField(max_length=200,
                                   choices=(('Proceso', 'Proceso'),
                                            ('Estado', 'Estado'),
                                            ('NUEVO_Proceso', 'NUEVO_Proceso'),
                                            ('NUEVO_Estado', 'NUEVO_Estado')))

    def __unicode__(self):
        return u"%s" % self.name


class MentalEdge(models.Model):
    ego = models.ForeignKey(Alter, null=True)
    source = models.ForeignKey(Variable,
                               related_name='leads_to',
                               null=True)
    target = models.ForeignKey(Variable,
                               related_name='caused_by',
                               null=True)

    phase = models.ForeignKey(Phase, null=True)

    def __unicode__(self):
        return u"(%s)->(%s)" % (self.source, self.target)


class Networks:
    def __init__(self, phase):

        self.phase = phase
        self.alter = nx.Graph()

        for e in EgoEdge.objects.filter(phase=phase):
            self.alter.add_edge(e.source, e.target,
                                distance=e.distance,
                                interaction=e.interaction)

    def update_alter_metrics(self):
        degrees = list(self.alter.degree())
        for node in degrees:
            node[0].degree = node[1]
            node[0].save()

    def update_action_metrics(self):
        for a in Action.objects.all():
            a.update_in_degree(self.phase)
            a.save()


class AgencyNetwork:
    def __init__(self, ego_ids, phase_id):
        phase = Phase.objects.get(pk=phase_id)
        g = nx.DiGraph()
        for ego_id in ego_ids:
            ego = Alter.objects.get(id=ego_id)

            # create network from egos to alters
            for e in ego.ego_net.filter(phase=phase):
                if e.source.name.startswith('TL0'):
                    g.add_node(e.source.id,
                               name=e.source.name,
                               shape="ellipse",
                               width=260,
                               height=260,
                               avatar=e.source.avatar_url(),
                               href='/alter/%s/' % e.source.id,
                               scolor=colors.sector_color(e.source))
                else:
                    g.add_node(e.source.id,
                               name=e.source.name,
                               shape="ellipse",
                               width=160,
                               height=100,
                               href='/alter/%s/' % e.source.id,
                               scolor=colors.sector_color(e.source))
                for action_e in ActionEdge.objects.filter(
                        alter=e.source).filter(phase=phase):
                    g.add_node(action_e.action.action,
                               name=action_e.action.action,
                               shape='rectangle',
                               width=160,
                               height=100,
                               href='/action/%s/' % action_e.action.id,
                               scolor=colors.practice_color(
                                   action_e.action))
                    g.add_edge(action_e.alter.id,
                               action_e.action.action)

                if e.target.name.startswith('TL0'):
                    g.add_node(e.target.id,
                               name=e.target.name,
                               shape="ellipse",
                               width=260,
                               height=260,
                               avatar=e.target.avatar_url(),
                               href='/alter/%s/' % e.target.id,
                               scolor=colors.sector_color(e.target))
                else:
                    g.add_node(e.target.id,
                               name=e.target.name,
                               shape="ellipse",
                               width=160,
                               height=100,
                               href='/alter/%s/' % e.target.id,
                               scolor=colors.sector_color(e.target))
                for action_e in ActionEdge.objects.filter(
                        alter=e.target).filter(phase=phase):
                    g.add_node(action_e.action.action,
                               name=action_e.action.action,
                               shape='rectangle',
                               width=160,
                               height=100,
                               href='/action/%s/' % action_e.action.id,
                               scolor=colors.practice_color(
                                   action_e.action))
                    g.add_edge(action_e.alter.id,
                               action_e.action.action)

                g.add_edge(e.source.id,
                           e.target.id,
                           distance=4 - e.distance,
                           polarity=e.polarity,
                           i_s=e.influence_source,
                           i_t=e.influence_target)

        self.g = g

    def get_json(self):
        net = {'nodes': [{'data': {'id': n,
                                   'href': self.g.node[n]['href'],
                                   'name': self.g.node[n]['name'],
                                   'shape': self.g.node[n]['shape'],
                                   'width': self.g.node[n]['width'],
                                   'height': self.g.node[n]['height'],
                                   'avatar': "%s"
                                   % self.g.node[n].get('avatar', '/media/'),
                                   'scolor': self.g.node[n]['scolor']}}
                         for n in self.g.nodes],
               'edges': [{'data':
                          {'source': e[0],
                           'target': e[1],
                           'source_label': self.g.get_edge_data(
                               *e).get('i_s', ''),
                           'target_label': self.g.get_edge_data(
                               *e).get('i_t', ''),
                           'distance': self.g.get_edge_data(
                               *e).get('distance', 0),
                           'polarity': "crimson"
                           if self.g.get_edge_data(*e).get('polarity', 0) == -1
                           else "cornflowerblue"
                           if self.g.get_edge_data(*e).get('polarity', 0) == 1
                           else "grey"}}
                         for e in self.g.edges]}
        return net


class MentalModel:
    def __init__(self, ego_ids, phase_id):
        phase = Phase.objects.get(pk=phase_id)
        g = nx.DiGraph()
        for ego_id in ego_ids:
            ego = Alter.objects.get(id=ego_id)
            h = ego.mental_model(phase)

            g = nx.compose(g, h)

        for ego_id in ego_ids:
            ego = Alter.objects.get(id=ego_id)
            h = ego.mental_model(phase)
            for n in h.nodes:
                if n in g.nodes:
                    if 'egos' in g.node[n]:
                        g.node[n]['egos'].append(ego)
                    else:
                        g.node[n]['egos'] = [ego, ]

        self.g = g

    def get_json(self):
        net = {'nodes': [{'data': {'id': n,
                                   'shape': self.g.node[n]['shape']}}
                         for n in self.g.nodes],
               'edges': [{'data': {'source': e[0],
                                   'target': e[1]}} for e in self.g.edges]}
        return net

    def get_compound_json(self):

        net = {
            'nodes': [
                {'data': {'id': n, 'name': n}}
                for n in self.g.nodes],
            'edges': [{'data': {'source': e[0],
                                'target': e[1]}} for e in self.g.edges]}

        i = 0
        for n in self.g.nodes:
            for ego in self.g.node[n]['egos']:
                net['nodes'].append({'data': {'id': ego.name + " " + str(i),
                                              'name': ego.name,
                                              'parent': n}})
                i += 1
        return net


class PowerNetwork:
    def __init__(self, ego_ids, phase_id):
        phase = Phase.objects.get(pk=phase_id)
        g = nx.Graph()
        for ego_id in ego_ids:
            ego = Alter.objects.get(id=ego_id)
            h = ego.power_network(phase)
            g = nx.compose(g, h)

        self.g = g

    def get_json(self):
        net = {'nodes': [{'data': {'id': n,
                                   'shape': self.g.node[n]['shape'],
                                   'width': self.g.node[n]['width'],
                                   'height': self.g.node[n]['height'],
                                   'avatar': "%s"
                                   % self.g.node[n].get('avatar', '/media/')}}
                         for n in self.g.nodes],
               'edges': [{'data': {'source': e[0],
                                   'target': e[1]}} for e in self.g.edges]}
        return net
