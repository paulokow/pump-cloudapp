# Create your views here.

from django.template import loader, Context
from .models import AllEvents, BGMeasure, Boluses
from datetime import datetime, timedelta
from pandas.core.frame import DataFrame
import numpy as np

# Create your views here.

from django.http import HttpResponse

def index(request):
  #msr = BGMeasure.objects.order_by('-timestamp')[:10]
  dt_start = datetime.today().date() - timedelta(days=1)
  msr = AllEvents.objects.filter(type = "BloodGlucoseReadingEvent", timestamp__gt = dt_start).order_by('-timestamp')
  bol = AllEvents.objects.filter(type = "NormalBolusDeliveredEvent", timestamp__gt = dt_start).order_by('-timestamp')
  template = loader.get_template('xxx/index.html')
  ctx = Context(
      {
          'measures': msr,
          'boluses': bol,
      })
  return HttpResponse(template.render(context=ctx))


def percentile(n):
  def percentile_(x):
    return np.percentile(x, n)
  percentile_.__name__ = 'percentile_%s' % n
  return percentile_

def testFill(request):
  #msr = BGMeasure.objects.order_by('-timestamp')[:10]
  dt_start = datetime.today().date() - timedelta(days=14)
  msr_tmp = BGMeasure.objects.filter(timestamp__gt = dt_start).order_by('timestamp')
  msr = []
  last_it = None
  for it in msr_tmp:
    if last_it != None:
      diff = it.timestamp - last_it.timestamp
      diff_hours = (int) (diff.seconds // (60 *60))
      if it.timestamp.minute > last_it.timestamp.minute:
        diff_hours -= 1
      if (diff_hours > 0):
        step_time = diff / (diff_hours + 1)
        step_value = (it.value - last_it.value) / (diff_hours + 1)
        for idx in range(1, diff_hours + 1):
          newItem = {}
          ts = last_it.timestamp + idx * step_time
          newItem["day"] = ts.day
          newItem["hour"] = ts.hour
          newItem["value"] = last_it.value + idx * step_value
          msr.append(newItem)
    newIt = {}
    newIt["day"] = it.timestamp.day
    newIt["hour"] = it.timestamp.hour
    newIt["value"] = it.value
    msr.append(newIt)
    last_it = it
  frame = DataFrame(msr)
  by_hour_and_day = frame.groupby(['day', 'hour']).mean()
  
  daily_avg = by_hour_and_day.groupby(['hour']).mean()
  daily_min = by_hour_and_day.groupby(['hour']).min()
  daily = by_hour_and_day.groupby(['hour']).agg([np.min, np.max, np.mean, percentile(15), percentile(85)])
  
  template = loader.get_template('xxx/index2.html')  
  ctx = Context(
      {
          'measures': daily,
      })
      
  return HttpResponse(template.render(context=ctx))
