# -*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from planlos.termine.models import Termin, Location, Regular
from planlos.blog.models import Entry
import datetime

class Termine_Syndication(Feed):
    title = "Planlos Bremen (Termine)"
    link = "/termine"
    description = "Alle Termine die neu eingetragen werden"

    def items(self):
        today = datetime.datetime.now()
        return Termin.objects.filter( is_pub=True, datum__gte=today, datum__lte=today+datetime.timedelta(30) ).order_by('-datum')[:30]

class Heute_Syndication(Feed):
    title = "Planlos Bremen (Was geht heute?)"
    link = "/termine/heute"
    description = "Alle Termine für den aktuellen Tag"

    def items(self):
        today = datetime.datetime.now()
        return Termin.objects.filter( is_pub=True, datum=today ).order_by('-datum')

class Admin_Syndication(Feed):
    title = "Planlos Bremen Admin Interface (unbestätigte Termine)"
    link = "/admin/"
    description = "Alle Termine unbestätigten Termine"

    def items(self):
        today = datetime.datetime.now()
        return Termin.objects.exclude( is_pub=True).filter(datum__gte=today).order_by('-datum')


class Blog_Syndication(Feed):
    title = "Planlos Bremen (aktuelles)"
    link = "/aktuelles"
    description = "Neuigkeiten rund um Planlos"

    def items(self):
        return Entry.objects.order_by('-pub_date')[:10]

    def item_link(self):
        # entweder diese funktion oder eine get_absolute_urls für blog_entry
        return "http://planlosbremen.de/aktuelles"
