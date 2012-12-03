#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.db import models
from django.contrib.auth import models as authmodel
from django.utils.encoding import smart_unicode
# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    selfportrait = models.TextField(blank=True)
    url = models.URLField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images/location/', blank=True)
    streetmap = models.ImageField(upload_to='images/location/streetmaps/', blank=True)

    def get_absolute_url(self):
        return "/termine/location/%i/" % self.id

    def __unicode__(self):
        return smart_unicode(self.name)

    class Meta:
	ordering = ['name']



class Action_Type(models.Model):
    type = models.CharField(max_length=60)

    def __unicode__(self):
        return smart_unicode(self.type)

    class Meta:
        ordering = ['type']

class Link_Category(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()

    def __unicode__(self):
        return smart_unicode(self.name)

class Link(models.Model):
    name = models.CharField(max_length=100)
    category =  models.ForeignKey(Link_Category)
    url = models.URLField(max_length=100)

    def __unicode__(self):
        return smart_unicode(self.name)

class Regular(models.Model):
    REPEATER_CHOICES = (
        ('1', 'Jeden 1.'),
        ('2', 'Jeden 2.'),
        ('3', 'Jeden 3.'),
        ('4', 'Jeden 4.'),
        ('1,2,3,4', 'Jeden (1.,2.,3.,4.)'),
        ('1,2', 'Jeden 1. + 2.'),
        ('1,3', 'Jeden 1. + 3.'),
        ('1,2,3', 'Jeden 1. + 2. + 3.'),
        ('2,3', 'Jeden 2. + 3.'),
        ('2,4', 'Jeden 2. + 4.'),
        ('3,4', 'Jeden 3. + 4.'),
        )

    DAY_CHOICES = (
        (0, "Montag"),
        (1, "Dienstag"),
        (2, "Mittwoch"),
        (3, "Donnerstag"),
        (4, "Freitag"),
        (5, "Samstag"),
        (6, "Sonntag"),
        )


    title = models.CharField(max_length=70)
    short_desc = models.TextField()
    desc = models.TextField(blank=True)
    time = models.TimeField('Uhrzeit')
    type = models.ForeignKey(Action_Type, blank=True)

    repeater = models.CommaSeparatedIntegerField(max_length=8, choices=REPEATER_CHOICES)
    day = models.IntegerField(choices=DAY_CHOICES)

    group = models.ForeignKey(authmodel.User)
    location = models.ForeignKey(Location)
    room = models.CharField(max_length=20, blank=True)
    is_pub = models.BooleanField()
    exturl = models.URLField(max_length=100, blank=True)

    def __unicode__(self):
        return smart_unicode(self.title)

    def get_absolute_url(self):
        return "/termine/regular/%i/" % self.id


## Sachen die länger dauern
## G8, Filmtage, etc.

class Action_Period(models.Model):
    start_date = models.DateField('begin')
    end_date = models.DateField('end')
    title = models.CharField(max_length=70)
    short_desc = models.CharField(max_length=120)
    desc = models.TextField(blank=True)
    exturl = models.URLField(max_length=100, blank=True)
    is_pub = models.BooleanField()
    group = models.ForeignKey(authmodel.User)
    location = models.ForeignKey(Location, blank=True)

    def __unicode__(self):
        return smart_unicode(self.start_date)+ u" - " + smart_unicode(self.end_date)

class Termin(models.Model):
    datum = models.DateField('date')
    time = models.TimeField('Uhrzeit')
    type = models.ForeignKey(Action_Type)
    title = models.CharField(max_length=70)
    short_desc = models.CharField(max_length=120, blank=True)
    desc = models.TextField(blank=True)
    exturl = models.URLField(max_length=100, blank=True)
    is_pub = models.BooleanField()
    group = models.ForeignKey(authmodel.User)
    location = models.ForeignKey(Location)
    room = models.CharField(max_length=20, blank=True)
    flyer = models.ImageField(upload_to='images/flyer/', blank=True)

    def __unicode__(self):
        return smart_unicode(self.title+" "+smart_unicode(self.datum))

    def get_absolute_url(self):
        return "/termine/termin/%i/" % self.id

class Permanent_Flyer(models.Model):
    termin = models.ForeignKey(Termin)

    def __unicode__(self):
        return smart_unicode(smart_unicode(self.termin.title))



class Feature(models.Model):
    comment = models.CharField(max_length=400)
    event = models.ForeignKey(Termin)

