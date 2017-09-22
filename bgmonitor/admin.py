# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import BGMeasure
from .models import Boluses

admin.site.register(BGMeasure)
admin.site.register(Boluses)
