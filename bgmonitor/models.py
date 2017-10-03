# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from _weakref import proxy

# Create your models here.

class AllEvents (models.Model):
    class Meta:
        db_table = 'all_events'
            
    type = models.TextField()
    timestamp = models.DateTimeField()
    hour = models.IntegerField()

    #BGMeasure 
    value = models.IntegerField(null=True)

    #Boluses
    delivered = models.FloatField(null=True)
    programmed = models.FloatField(null=True)
    
    #BolusWizard
    bgInput = models.IntegerField(null=True)
    carbInput = models.IntegerField(null=True)
    carbRatio = models.FloatField(null=True)
    correctionEstimate = models.IntegerField(null=True)
    bolusWizardEstimate = models.IntegerField(null=True)
    estimateModifiedByUser = models.IntegerField(null=True)
    finalEstimate = models.IntegerField(null=True)    
    
    #Basal
    rate = models.FloatField(null=True)
    patternName = models.TextField(null=True)      
    
    def __init__(self, *args, **kwargs):
        super(AllEvents, self).__init__(*args, **kwargs)
        if self.type == "BloodGlucoseReadingEvent":
            self.__class__ = BGMeasure
        elif self.type == "NormalBolusDeliveredEvent":
            self.__class__ = Boluses            
        elif self.type == "BolusWizardEstimateEvent":
            self.__class__ = BolusWizard            
        elif self.type == "BasalSegmentStartEvent":
            self.__class__ = Basal            
          
class BGMeasureManager(models.Manager):
    def get_query_set(self):
        return super(BGMeasureManager, self).get_query_set().filter(
        	type='BloodGlucoseReadingEvent')

class BGMeasure (AllEvents):
    objects = BGMeasureManager()
    class Meta:
        proxy = True

class BolusesManager(models.Manager):
    def get_query_set(self):
        return super(BolusesManager, self).get_query_set().filter(
        	type='NormalBolusDeliveredEvent')

class Boluses (AllEvents):
    objects = BolusesManager()
    class Meta:
        proxy = True

class BolusWizardManager(models.Manager):
    def get_query_set(self):
        return super(BolusWizardManager, self).get_query_set().filter(
        	type='BolusWizardEstimateEvent')

class BolusWizard (AllEvents):
    objects = BolusWizardManager()
    class Meta:
        proxy = True

class BasalManager(models.Manager):
    def get_query_set(self):
        return super(BasalManager, self).get_query_set().filter(
        	type='BasalSegmentStartEvent')

class Basal (AllEvents):
    objects = BasalManager()
    class Meta:
        proxy = True
