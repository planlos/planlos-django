# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def newurl(request):
	return HttpResponse("Neue Adresse: http://planlosbremen.de")
