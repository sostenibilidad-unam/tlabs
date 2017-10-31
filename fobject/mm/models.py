# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class Sector(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class Alter(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(Type, null=True)
    sector = models.ForeignKey(Sector, null=True)
    desc = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % self.name


class EgoEdge(models.Model):
    source = models.ForeignKey(Alter, related_name='ego_net')
    target = models.ForeignKey(Alter, related_name='alter_for')

    distance = models.IntegerField()
    interaction = models.CharField(max_length=20)

    def __unicode__(self):
        return u"%s<-%s->%s" % (self.source, self.distance, self.target)


class Action(models.Model):
    accion = models.CharField(max_length=200)

    def __unicode__(self):
        return u"!%s" % self.accion


class Agency(models.Model):
    alter = models.ForeignKey(Alter,
                              related_name='action_set',
                              null=True)
    action = models.ForeignKey(Action,
                               related_name='actor_set',
                               null=True)

    def __unicode__(self):
        return u"%%s->%s" % (self.alter, self.accion)


class MentalType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return u"%s" % self.name


class Item(models.Model):
    type = models.ForeignKey(MentalType)


class MentalEdge(models.Model):
    source = models.ForeignKey(Item,
                               related_name='leads_to',
                               null=True)
    target = models.ForeignKey(Item,
                               related_name='caused_by',
                               null=True)
