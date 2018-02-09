# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, EgoEdge, Action, Fase, \
    Sector, ActionEdge, Variable, MentalEdge, Category


class AlterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'sector', 'avatar_name', 'image_tag']


admin.site.register(Alter, AlterAdmin)


class EgoEdgeAdmin(admin.ModelAdmin):
    search_fields = ['source__name', 'target__name', 'fase']
    list_display = ['id', 'source', 'target', 'distance', 'fase']


admin.site.register(EgoEdge, EgoEdgeAdmin)


admin.site.register(Sector)
admin.site.register(Fase)
admin.site.register(Category)
admin.site.register(Variable)


class ActionAdmin(admin.ModelAdmin):
    search_fields = ['action', ]
    list_display = ['id', 'action', 'category', 'in_degree']


admin.site.register(Action, ActionAdmin)


class ActionEdgeAdmin(admin.ModelAdmin):
    search_fields = ['alter__name', 'action__action']
    list_display = ['alter', 'action', 'fase']


admin.site.register(ActionEdge, ActionEdgeAdmin)


class MentalEdgeAdmin(admin.ModelAdmin):
    search_fields = ['ego__name']
    list_display = ['ego', 'source', 'target', 'fase']


admin.site.register(MentalEdge, MentalEdgeAdmin)
