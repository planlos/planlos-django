# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from planlos.termine.models import Termin, Location, Regular, Action_Period, Action_Type
from django import forms
# development release
from django.forms import ModelForm
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import InvalidPage
from django.core.context_processors import csrf
from django.db.models import Q


import datetime
from kalender_helpers import *

def linklist(request):
    pass

def whereisall(request):
    locations = Location.objects.all()
    t = loader.get_template('termine/whereisall.html')
    c = Context({'locations': locations } )
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def get_regulars(day):
    regulars = Regular.objects.filter( is_pub=True, day=day.weekday())
    first_day_of_month = datetime.datetime(day.year, day.month, 1)
    day_count = 0
    while first_day_of_month <= day:
        if first_day_of_month.weekday() == day.weekday():
            day_count +=1
        first_day_of_month += datetime.timedelta(1)
    day_reg = []
    for i in regulars:
        for j in i.repeater:
            try:
                if int(j) == day_count:
                    day_reg.append(i)
                    continue
            except:
                pass
    return day_reg

def day(request, year, month, day):
    today = datetime.datetime(int(year), int(month), int(day))
    if request.user.is_superuser:
    	thisday = Termin.objects.filter(datum=today)
    else:
    	thisday = Termin.objects.filter(datum=today).filter( Q(is_pub=True) | Q(group=request.user))

    weekday = today.weekday()
    regulars = get_regulars(today)
    t = loader.get_template('termine/day.html')
    c = Context({'entries': thisday, 'today' : today, 'regulars': regulars, 'weekday': weekday } )
    c.update(csrf(request))
    return HttpResponse(t.render(c))


def overview(request):
    today = datetime.datetime.now()
    this_month = today + datetime.timedelta(31)
    month_entries = []
    # filter
    types = Action_Type.objects.all()
    filters = {0: "alle Veranstaltungen"}
    for i in types:
        filters[i.pk] = i.type

    for i in range(31):
        entries = []
        day = today + datetime.timedelta(i)
        filter_type = 0
        if request.method == 'POST':
            filter_type = int(request.POST['type_filter'])
        if filter_type != 0:
            entries = Termin.objects.filter( Q(is_pub=True) | Q(group=request.user) ).filter(datum=day).filter(type=filter_type)
        else:
            entries = Termin.objects.filter( Q(is_pub=True) | Q(group=request.user) ).filter(datum=day)
        if len(entries) > 0:
            month_entries.append( (day, entries) )
    reg_today = get_regulars( datetime.datetime.now() )
    t = loader.get_template('termine/overview.html')
    c = Context({'today': today,
                 'entries': month_entries,
                 'filter_type': filter_type,
                 'filters': filters,
                 'regulars_today': reg_today } )
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def nextdays(request, diff = 0):
    nday = datetime.datetime.now() + datetime.timedelta(diff)
    title = "Heute"
    if diff == 1:
        title = "Morgen"
    elif diff == 2:
        title = "Übermorgen"
    entries = Termin.objects.filter( Q(is_pub=True) | Q(group=request.user) ).filter(datum=nday ).order_by('datum')
    regulars = get_regulars( nday)
    c = Context({'today': nday,
                 'title': title,
                 'entries': entries,
                 'regulars': regulars })
    c.update(csrf(request))
    t = loader.get_template('termine/day.html')
    return HttpResponse(t.render(c))

### Whole publish thingy

class P_Form(ModelForm):
    datum = forms.DateField(widget=forms.TextInput(attrs={'class':"vDateField required"}))
    time = forms.TimeField(widget=forms.TextInput(attrs={'class':"vTimeField required"}))
    class Meta:
        model = Termin
        exclude = ('is_pub', 'group')

@login_required
def create_entry(request):
    if request.method == 'POST':
        instance = Termin(group=request.user)
        #new_data = request.POST.copy() 
        #new_data.update(request.FILES)  # This has to be added 
        if request.FILES.has_key("flyer"):
            #flyer_file = request.FILES["flyer"]
            #file_data = {'flyer': {'filename': flyer_file.name,
            #                       'content': flyer_file.read()}}
            form = P_Form(request.POST, request.FILES, instance=instance)
        else:
            form = P_Form(request.POST, instance=instance)
        if form.is_valid():
            #form.save_source_file(form.cleaned
            form.save()
            return HttpResponseRedirect('/termine/publish/')
        else:
            t = loader.get_template('termine/create_entry.html')
            c = Context( {'user': request.user, 'terminform': form} )
            c.update(csrf(request))
            return HttpResponse(t.render(c))
    else:
        ne = P_Form()
        t = loader.get_template('termine/create_entry.html')
        c = Context( {'user': request.user, 'terminform': ne} )
        c.update(csrf(request))
        return HttpResponse(t.render(c))

@login_required
def publish(request):
    today = datetime.datetime.today()
    u = request.user
    f = P_Form()
    s = f.as_p()
    gentries = Termin.objects.filter(group=u).exclude(datum__lt=today).order_by('datum')
    oentries = Termin.objects.all().exclude(group=u).exclude(datum__lt=today).order_by('datum')
    t = loader.get_template('termine/publish_view.html')
    c = Context({'group_entries': gentries, 'other_entries': oentries, 'user': u, 'group': u, 'terminform': s } )
    c.update(csrf(request))
    return HttpResponse(t.render(c))

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/termine/')

def may_edit(u, entry):
    if ( entry.group == u ):
        return True
    else:
        return False

@login_required
def edit(request, termin_id):
    entry = get_object_or_404(Termin, pk=termin_id)
    if may_edit(request.user, entry):
        if request.method == 'POST':
            u = request.user
            #instance = Termin(group=u, is_pub=True)
            instance = entry
            #new_data = request.POST.copy()
            #new_data.update(request.FILES)  # This has to be added
            if request.FILES.has_key("flyer"):
                #flyer_dict = request.FILES["flyer"]
                #file_data = {'flyer': {'filename': flyer_dict["filename"],
                #                       'content': flyer_dict["content"] }}
                form = P_Form(request.POST, request.FILES, instance=instance)
            else:
                form = P_Form(request.POST, instance=instance)
            if form.is_valid():
                #form.pk = entry.pk
                #entry.delete()
                form.save()
                return HttpResponseRedirect('/termine/publish/')
            else:
                t = loader.get_template('termine/edit_entry.html')
                c = Context({'terminform': form, 'termin_id' : termin_id } )
                c.update(csrf(request))
                return HttpResponse(t.render(c))
        else:
            g = P_Form(instance=entry)
            t = loader.get_template('termine/edit_entry.html')
            c = Context({'terminform': g, 'termin_id' : termin_id } )
            c.update(csrf(request))
            return HttpResponse(t.render(c))
        #return HttpResponse( fs+g.as_p()+fs2 )
    else:
        return HttpResponse("Keinen Zugriff")

@login_required
def fast_admin(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Nix da!")
    if request.method == 'POST':
        s = ''
        for item in request.POST.iteritems():
            try:
                t = Termin.objects.get(id=item[1])
                t.is_pub = True
                t.save()
		# with wsgi print is not possible
                #print "DEBUG: item.id", item[1]
            except:
		pass
                #print "Fast_Admin: unknown Termin object:", item[1]
        #return HttpResponse(s)
        # get id and change pub
        return HttpResponseRedirect('/termine/publish/')
    else:
        today = datetime.datetime.today()
        unpublished = Termin.objects.filter(is_pub=False).filter(datum__gt=today).order_by('-datum')

        t = loader.get_template('termine/fast_admin.html')
        c = Context( { 'unpublished': unpublished } )
        c.update(csrf(request))
        return HttpResponse( t.render(c) )
    
