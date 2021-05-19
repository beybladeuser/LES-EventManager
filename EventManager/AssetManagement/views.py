from django.shortcuts import render
from django.http import HttpResponse
from .models import Asset
from .models import Service
from .models import Asset, Equipment, Rooms, Service
from django.template import loader

from .forms import *


# Create your views here.
def home(request) :
    template = loader.get_template('home.html')
   
    context = {
    }

    return HttpResponse(template.render(context, request))


def consultar_assets(request):
    template = loader.get_template('ViewAssets.html')
    context = {
        'Assets': Asset.objects.all()
    }
    return HttpResponse(template.render(context, request))

    
def consultar_services(request):
    template = loader.get_template('ViewServices.html')
    context = {
        'Services': Service.objects.all()
    }
    return HttpResponse(template.render(context, request))

def consultar_equipments(request):
    template = loader.get_template('ViewEquipments.html')
    context = {
        'Equipments': Equipment.objects.all()
    }
    return HttpResponse(template.render(context, request))

def consultar_rooms(request):
    template = loader.get_template('ViewRooms.html')
    context = {
        'Rooms': Rooms.objects.all()
    }
    return HttpResponse(template.render(context, request))    



def insert_assets(request):
    if request.method == 'POST':
        iaf = InsertAssetForm(request.POST)
    
    template = loader.get_template('InsertAssets.html')
    context = {
       'InsertAssetForm': iaf
    }
    return HttpResponse(template.render(context, request))    

