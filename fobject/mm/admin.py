# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, Type, EgoEdge, Action, \
    Sector, Agency, MentalType, Item, MentalEdge, Category


class AlterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'sector']


admin.site.register(Alter, AlterAdmin)


class EgoEdgeAdmin(admin.ModelAdmin):
    search_fields = ['source__name', 'target__name']
    list_display = ['id', 'source', 'target', 'distance']


admin.site.register(EgoEdge, EgoEdgeAdmin)


admin.site.register(Type)
admin.site.register(Sector)

admin.site.register(Category)


class ActionAdmin(admin.ModelAdmin):
    search_fields = ['action', ]
    list_display = ['id', 'action', 'category', 'in_degree']


admin.site.register(Action, ActionAdmin)


class AgencyAdmin(admin.ModelAdmin):
    search_fields = ['alter__name', 'action__action']
    list_display = ['alter', 'action']


admin.site.register(Agency, AgencyAdmin)

admin.site.register(MentalType)
admin.site.register(Item)
admin.site.register(MentalEdge)
