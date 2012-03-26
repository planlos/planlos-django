from django import template
from datetime import datetime, date, timedelta
import calendar
from planlos.termine.models import Termin, Regular, Feature
from planlos.polls.models import Poll, Choice
import random

register = template.Library()

@register.inclusion_tag('termin_bar.html')
def show_termine():
    today = datetime.today()
    this_month = today + timedelta(31)
    termine = Termin.objects.filter( is_pub=True ).filter(datum__range=(today, this_month) ).order_by('datum')[:5]
    return {'termine': termine }


@register.inclusion_tag('rotation_flyer.html')
def show_rot_flyer():
    today = datetime.today()
    termin_with_flyer = Termin.objects.exclude(is_pub=False).exclude(flyer='').exclude(datum__lt=today)
    c = termin_with_flyer.count()
    if c:
        ri = random.randint(0, c-1)
        flyer = termin_with_flyer[ri]
        return {'flyer': flyer }
    else:
        return {'flyer': 0 }


@register.inclusion_tag('featured_event.html')
def show_featured_event():
    featured_event = Feature.objects.all()
    if featured_event.count() > 0:
	return {'event': featured_event[0].event, 'comment': featured_event[0].comment}
    else:
	return {'event': None } 


@register.inclusion_tag('cal_tag.html')
def show_calendar(day):
    today = date.today()
    current_calendar = build_calendar(int(today.year), int(today.month) )
    next_today = today + timedelta(weeks=4)
    next_calendar = build_calendar(int(next_today.year), int(next_today.month) )
    return {'current_calendar': current_calendar, 'next_calendar': next_calendar, 'today': today, 'next_today': next_today }

def build_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    entries = Termin.objects.filter( is_pub=True, datum__month=month )
    ncal = []
    for week in cal:
        nweek = []
        for day in week:
            nweek.append( [day, False] )
            if day:
                dday = date(year, month, day)
                for j in entries:
                    if j.datum == dday:
                        nweek[-1][1] = True
        ncal.append(nweek)
    while len(ncal) < 6:
        ncal.append ( [ [0, False],[0, False],[0, False],
                        [0, False],[0, False],[0, False],[0, False] ] )
    return ncal

@register.inclusion_tag('last_vote.html')
def last_vote():
    today = datetime.now()
    poll = Poll.objects.filter(close_date__gt=today)[0]
    choices = Choice.objects.filter(poll=poll)
    return {'poll': poll, 'choices': choices}

@register.filter('makerange')
def makerange(value):
    return range(1,value+1)
