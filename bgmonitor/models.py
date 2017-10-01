# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from _weakref import proxy

# Create your models here.

class AllEvents (models.Model):
    class Meta:
        db_table = 'all_values'
            
    type = models.TextField()
    timestamp = models.DateTimeField()
    hour = models.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AllEvents, self).__init__(*args, **kwargs)
        if self.type == "BloodGlucoseReadingEvent":
            self.__class__ = "BGMeasure"
        elif self.type == "NormalBolusDeliveredEvent":
            self.__class__ = "Boluses"            
          
class BGMeasure (AllEvents):
    class Meta:
        proxy = True
    
    value = models.IntegerField()

class Boluses (AllEvents):
    class Meta:
        proxy = True
        
    delivered = models.FloatField()
    programmed = models.FloatField()
