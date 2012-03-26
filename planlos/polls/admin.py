#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import Poll, Choice, Hashtable
from django.contrib import admin

admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Hashtable)
