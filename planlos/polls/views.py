#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create your views here.

from models import Poll, Choice, Hashtable

from django.shortcuts import *
import datetime
#import hashlib
import sha

def show_results(request, pollid):
    poll = get_object_or_404(Poll, pk=pollid)
    choices = Choice.objects.all().filter(poll=poll)
    sum = 0
    for i in choices:
        sum += i.votes
    graph = {}
    for i in choices:
        graph[i.choice] = (100.0/sum) * i.votes
    return render_to_response('polls/show_results.html', {'poll': poll, 'graph': graph, 'num_votes': sum})


def show_poll(request, pollid):
    poll = get_object_or_404(Poll, pk=pollid)
    choices = Choice.objects.all().filter(poll=poll)
    return render_to_response('polls/show_poll.html', {'poll': poll, 'choices': choices})

def vote(request, pollid):
    poll = get_object_or_404(Poll, pk=pollid)
    date_now = datetime.datetime.now()
    
    ipaddr = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']
    #sha1 = hashlib.sha1()
    sha1 = sha.sha()
    day = datetime.date.today()
    sha1.update(user_agent+ipaddr+str(day))
    r = Hashtable.objects.all().filter(poll=poll).filter(hash=sha1.hexdigest())
    if len(r) != 0:
        for i in r:
            if i.poll == poll:
                message = 'Es scheint als haettest Du diese Umfrage schon einmal mitgemacht'
                return render_to_response('polls/show_poll.html', {'poll': poll, 'message': message})
    else:
        h = Hashtable()
        h.poll = poll
        h.hash = sha1.hexdigest()
        h.save()
        
    if poll.close_date < date_now or poll.closed:
        message = 'Sorry, die Umfrage ist bereits abgelaufen'
        return render_to_response('polls/show_poll.html', {'poll': poll, 'choices': choices, 'message': message})
    if request.method == 'POST':
        if request.POST.has_key("choice"):
            choiceid = int(request.POST['choice'])
            choice = get_object_or_404(Choice, pk=choiceid)
            if choice.poll != poll:
                return HttpResponse("Wrong")
            choice.votes += 1
            choice.save()
            message = 'Danke, fuer deine Meinung'
            return render_to_response('polls/show_poll.html', {'poll': poll, 'message': message})
    return render_to_response('polls/show_poll.html', {'poll': poll, 'choices': choices, 'message': message})

