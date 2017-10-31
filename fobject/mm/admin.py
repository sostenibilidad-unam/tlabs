# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, Type, EgoEdge, Action, \
    Sector, Agency, MentalType, Item, MentalEdge, Category

admin.site.register(Type)
admin.site.register(Sector)
admin.site.register(Alter)
admin.site.register(EgoEdge)

admin.site.register(Category)
admin.site.register(Action)
admin.site.register(Agency)

admin.site.register(MentalType)
admin.site.register(Item)
admin.site.register(MentalEdge)
