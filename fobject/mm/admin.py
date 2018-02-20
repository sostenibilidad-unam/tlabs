# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, EgoEdge, Action, Fase, \
    Sector, ActionEdge, Variable, MentalEdge, Category, \
    Power, PowerEdge


class AlterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'sector', 'avatar_name', 'image_tag']


admin.site.register(Alter, AlterAdmin)


class EgoEdgeAdmin(admin.ModelAdmin):
    search_fields = ['source__name', 'target__name', 'fase__fase']
    list_display = ['id', 'source', 'target', 'distance', 'fase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        fase = Fase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.fase = fase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(EgoEdge, EgoEdgeAdmin)


admin.site.register(Sector)
admin.site.register(Fase)
admin.site.register(Category)
admin.site.register(Variable)


class ActionAdmin(admin.ModelAdmin):
    search_fields = ['action', ]
    list_display = ['action', 'category', 'in_degree']


admin.site.register(Action, ActionAdmin)


class ActionEdgeAdmin(admin.ModelAdmin):
    search_fields = ['alter__name', 'action__action']
    list_display = ['id', 'alter', 'action', 'fase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        fase = Fase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.fase = fase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(ActionEdge, ActionEdgeAdmin)


class MentalEdgeAdmin(admin.ModelAdmin):
    search_fields = ['ego__name']
    list_display = ['ego', 'source', 'target', 'fase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        fase = Fase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.fase = fase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(MentalEdge, MentalEdgeAdmin)

admin.site.register(Power)


class PowerEdgeAdmin(admin.ModelAdmin):
    search_fields = ['ego__name', 'power__name']
    list_display = ['source', 'target', 'fase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        fase = Fase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.fase = fase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(PowerEdge, PowerEdgeAdmin)
