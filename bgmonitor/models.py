# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class BGMeasure (models.Model):
  class Meta:
    db_table = 'bg_valueses'
  timestamp = models.DateTimeField()
  value = models.IntegerField()
