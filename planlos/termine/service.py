# -*- coding: utf-8 -*-

from planlos.termine.models import Termin, Location, Regular
from planlos.blog.models import Entry
import datetime

from django.core import serializers
from django.http import HttpResponse

def heute(request):
    queryset = Termin.objects.filter( is_pub=True, datum=today )
    json_serializer = serializers.get_serializer("json")()
    response = HttpResponse( mimetype="text/json")
    json = json_serializer.serialize(queryset, ensure_ascii=False, stream=response)
    return response

def monat(request):
    today = datetime.datetime.now()
    queryset = Termin.objects.filter( is_pub=True, datum__gte=today, datum__lte=today+datetime.timedelta(30))
    json_serializer = serializers.get_serializer("json")()
    response = HttpResponse( mimetype="text/json")
    json = json_serializer.serialize(queryset, ensure_ascii=False, stream=response)
    return response


def location(request, location_id):
    location = Location.objects.get(pk=location_id)
    json_serializer = serializers.get_serializer("json")()
    response = HttpResponse( mimetype="text/json")
    json = json_serializer.serialize([location], ensure_ascii=False, stream=response)
    return response
	
