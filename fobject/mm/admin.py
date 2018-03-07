# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, EgoEdge, Action, Phase, \
    Sector, ActionEdge, Variable, MentalEdge, Category, \
    Power, PowerEdge


class EgoEdgeInline(admin.TabularInline):
    model = EgoEdge
    fk_name = 'source'
    extra = 1


class ActionEdgeInline(admin.TabularInline):
    model = ActionEdge
    fk_name = 'alter'
    extra = 0


class PowerEdgeInline(admin.TabularInline):
    model = PowerEdge
    fk_name = 'source'
    extra = 1


class MentalEdgeInline(admin.TabularInline):
    model = MentalEdge
    fk_name = 'ego'
    extra = 1


class AlterAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'sector', 'avatar_name', 'image_tag']

    inlines = [EgoEdgeInline,
               ActionEdgeInline,
               PowerEdgeInline,
               MentalEdgeInline]


admin.site.register(Alter, AlterAdmin)


class EgoEdgeAdmin(admin.ModelAdmin):
    search_fields = ['source__name', 'target__name', 'phase__phase']
    list_display = ['id', 'source', 'target', 'distance', 'phase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        phase = Phase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.phase = phase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(EgoEdge, EgoEdgeAdmin)


admin.site.register(Sector)
admin.site.register(Phase)
admin.site.register(Category)


class VariableAdmin(admin.ModelAdmin):
    list_display = ['name', 'mental_type']


admin.site.register(Variable, VariableAdmin)


class ActionAdmin(admin.ModelAdmin):
    search_fields = ['action', ]
    list_display = ['action', 'category', 'in_degree']


admin.site.register(Action, ActionAdmin)


class ActionEdgeAdmin(admin.ModelAdmin):
    search_fields = ['alter__name', 'action__action']
    list_display = ['id', 'alter', 'action', 'phase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        phase = Phase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.phase = phase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(ActionEdge, ActionEdgeAdmin)


class MentalEdgeAdmin(admin.ModelAdmin):
    search_fields = ['ego__name']
    list_display = ['ego', 'source', 'target', 'phase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        phase = Phase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.phase = phase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(MentalEdge, MentalEdgeAdmin)

admin.site.register(Power)


class PowerEdgeAdmin(admin.ModelAdmin):
    search_fields = ['ego__name', 'power__name']
    list_display = ['source', 'target', 'phase']

    actions = ['copy_to_latest_phase']

    def copy_to_latest_phase(self, request, queryset):
        phase = Phase.objects.last()
        for edge in queryset:
            edge.pk = None
            edge.phase = phase
            edge.save()
    copy_to_latest_phase.\
        short_description = "Copy selected edges to latest phase"


admin.site.register(PowerEdge, PowerEdgeAdmin)
