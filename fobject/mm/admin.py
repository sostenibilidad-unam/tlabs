# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Alter, Type, EgoEdge, Action

admin.site.register(Type)
admin.site.register(Alter)
admin.site.register(EgoEdge)

admin.site.register(Action)
