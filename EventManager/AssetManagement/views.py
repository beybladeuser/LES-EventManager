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
    
    Assets = Asset.objects.all()
   
    i = 0
    sizeofAssets = len(Assets)
    while i < sizeofAssets :
        if Asset.getServiceType(Assets[i]) is not None:
            Assets[i].subtype =  Asset.getServiceType(Assets[i])
            Assets[i].type = "Serviço"

        elif Asset.getEquipmentType(Assets[i]) is not None:
            print("epahYha")
            Assets[i].subtype = Asset.getEquipmentType(Assets[i])
            Assets[i].type = "Equipamento"

        elif Asset.getRoom(Assets[i]) is not None:
            Assets[i].type = "Sala/Anfiteatro"
            Assets[i].subtype = Asset.getRoom(Assets[i]).campus + " - " + Asset.getRoom(Assets[i]).buildingname 
        i += 1

    context = {
        'Assets': Assets
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
        form = insert_assets(request.POST)
        if form.isvalid():
            form.save()
        else:
            form.save()
    return render(request, 'InsertAssets', {'InsertAssetForm': form})    

