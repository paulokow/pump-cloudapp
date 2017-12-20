# Create your views here.

from django.template import loader, Context, RequestContext
from .models import *
from datetime import datetime, timedelta
from pandas.core.frame import DataFrame
import numpy as np
from django.shortcuts import render_to_response

# Create your views here.

from django.http import HttpResponse


def main(request):
    return index(request, "bgmonitor/actual.html")

def main_details(request):
    return index(request, "bgmonitor/actual_details.html")
          
def index(request, template_file):
  try:
    dt_end = datetime.strptime(request.GET.get('end', ''), "%Y-%m-%d");  
  except ValueError:
    dt_end =  datetime.utcnow() 

  try:
    dt_start = datetime.strptime(request.GET.get('start', ''), "%Y-%m-%d");  
  except ValueError:
    dt_start =  dt_end - timedelta(days=2)  

  msr = BGMeasure.objects.filter(timestamp__gt = dt_start).filter(timestamp__lte = dt_end).order_by('-timestamp')
  bol = Boluses.objects.filter(timestamp__gt = dt_start).filter(timestamp__lte = dt_end).order_by('-timestamp')
  wiz = BolusWizard.objects.filter(timestamp__gt = dt_start).filter(timestamp__lte = dt_end).order_by('-timestamp')
  baz = Basal.objects.filter(timestamp__gt = dt_start).filter(timestamp__lte = dt_end).order_by('-timestamp')
  ctx = Context(
      {
          'dt_start': dt_start,
          'dt_end': dt_end,
          'mintime': dt_start,
          'maxtime': dt_end,
          'measures': msr,
          'boluses': bol,
          'wizardvalues': wiz,
          'basal': baz,
      })
  return render_to_response(template_file, ctx, context_instance=RequestContext(request))


def percentile(n):
  def percentile_(x):
    return np.percentile(x, n)
  percentile_.__name__ = 'percentile_%s' % n
  return percentile_

def stats(request):
  try:
    dt_end = datetime.strptime(request.GET.get('end', ''), "%Y-%m-%d");
  except ValueError:
    dt_end = datetime.today().date()

  try:
    dt_start = datetime.strptime(request.GET.get('start', ''), "%Y-%m-%d");
  except ValueError:
    dt_start =  dt_end - timedelta(days=14)

  msr_tmp = BGMeasure.objects.filter(timestamp__gt = dt_start).filter(timestamp__lte = dt_end).order_by('timestamp')
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
  
  ctx = Context(
      {
          'dt_start': dt_start,
          'dt_end': dt_end,
          'measures': daily,
      })
      
  return render_to_response('bgmonitor/stats.html', ctx, context_instance=RequestContext(request))
