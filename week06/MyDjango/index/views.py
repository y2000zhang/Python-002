from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from .models import Name

def index(request):
    return HttpResponse('Hello Django!')

def year(request,year):
    return HttpResponse(year)


def name(request,**kwargs):
    return HttpResponse(kwargs['name'])

def books(request):
    n = Name.objects.all()
    return render(request,'booklist.html',locals())