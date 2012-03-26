#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models



class Poll(models.Model):
    question = models.CharField(max_length=250)
    pub_date = models.DateTimeField()
    close_date = models.DateTimeField()
    closed = models.BooleanField()

    def __unicode__(self):
        return self.question


    def get_absolute_url(self):
        return "/polls/%i/" % self.id

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=250)
    votes = models.IntegerField()

    def __unicode__(self):
        return self.choice

class Hashtable(models.Model):
    hash = models.CharField(max_length=40)
    poll = models.ForeignKey(Poll)

    def __unicode__(self):
        return self.hash
