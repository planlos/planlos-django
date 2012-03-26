# new admin interface

from django.contrib import admin
from termine.models import *

class Termin_Admin(admin.ModelAdmin):
    list_filter = ['datum']
    list_display = ('datum', 'title', 'location', 'is_pub')
    # in Django SVN (exactly what i want, hmpf)
    #list_editable = ('is_pub')
    ordering = ['-datum']
    date_hierarchy = 'datum'
    fieldsets = [
            (None, {'fields': ('title', 'type')}),
            ('Zeit/Ort', {'fields': ('location', 'room', 'datum', 'time')}),
            (None, {'fields': ('short_desc', 'desc', 'exturl', 'group', 'flyer', 'is_pub')}),
            ]


class Link_Admin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url')
    ordering = ['category']

admin.site.register(Action_Period)
admin.site.register(Termin, Termin_Admin)
admin.site.register(Permanent_Flyer)
admin.site.register(Regular)
admin.site.register(Link, Link_Admin)
admin.site.register(Link_Category)
admin.site.register(Action_Type)
admin.site.register(Location)
admin.site.register(Feature)
