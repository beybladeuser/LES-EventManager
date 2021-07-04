from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Asset, Equipment, Rooms, Service

from AssetManagement.models import AssetType, Building
from PreEventManagement.models import AssetEvent

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .forms import *
from .tables import *


from .forms import *
from utilizadores.views import user_check
import PreEventManagement

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
            
        elif Asset.getEquipmentType(Assets[i]) is not None:
            Assets[i].subtype = Asset.getEquipmentType(Assets[i])
            
        elif Asset.getRoom(Assets[i]) is not None:
            room = Asset.getRoom(Assets[i])
            buildingg = Rooms.room_GetBuilding(room)
            
            Assets[i].subtype = Building.CampusName_BuildingName(buildingg)
        i += 1

    context = {
        'assetTypes': AssetType.getTypes(),
        # 'equipmentTypes': Equipmenttype.getEquipmenttypes(),
        # 'serviceTypes': Service.makeOptions(),
        # 'roomTypes': RoomType.getRoomTypes(),
        'Assets': Assets
    }
    return HttpResponse(template.render(context, request))

    
def consultar_services(request, isPreEdit = 0):
    template = loader.get_template('ViewServices.html')
    context = {
        'Services': Service.objects.all(),
         'isEdit': isPreEdit
    }
    return HttpResponse(template.render(context, request))

def consultar_equipments(request, isPreEdit = 0):

    template = loader.get_template('ViewEquipments.html')
    context = {
        'Equipments': Equipment.objects.all(),
        'isEdit': isPreEdit
    }
    return HttpResponse(template.render(context, request))


def consultar_rooms(request, isPreEdit = 0):
    template = loader.get_template('ViewRooms.html')
    rooms = Rooms.objects.all()
    for room in rooms:
        room = Rooms.getRoomWithCampus(room)
    context = {
        'Rooms': rooms,
        'isEdit': isPreEdit
    }
    return HttpResponse(template.render(context, request))    


def pre_delete_assets(request, assetID = None):
    template = loader.get_template('PreDeleteAssets.html')
    
    pre_delete_asset = Asset.objects.filter(id=assetID)
  

    if Asset.getServiceType(pre_delete_asset[0]) is not None:
        asset_subtype =  Asset.getServiceType(pre_delete_asset[0])
        asset_type = "Serviço"
    elif Asset.getEquipmentType(pre_delete_asset[0]) is not None:
        asset_subtype = Asset.getEquipmentType(pre_delete_asset[0])
        asset_type = "Equipamento"
    elif Asset.getRoom(pre_delete_asset[0]) is not None:
        room = Asset.getRoom(pre_delete_asset[0])
        buildingg = Rooms.room_GetBuilding(room)
        asset_type = "Sala/Anfiteatro"
        asset_subtype = Building.CampusName_BuildingName(buildingg)
    
    context = {
        'assetID': assetID,
        'asset_type': asset_type,
        'asset_subtype': asset_subtype,
        'asset': pre_delete_asset[0]
    }
    return HttpResponse(template.render(context, request))    


def delete_assets(request, assetID = None):

    pre_delete_asset = Asset.objects.filter(id=assetID)
    pre_delete_asset.id = assetID
    Asset.delete_asset(pre_delete_asset)

    return redirect('ViewAssets')


def edit_assets(request, assetID = None):
    if(Service.objects.filter(assetid=assetID).exists()):
        return redirect('EditService', assetID)
    
    elif(Equipment.objects.filter(assetid=assetID).exists()):
        return redirect('EditEquipment', assetID)
    
    elif(Rooms.objects.filter(assetid=assetID).exists()):
        return redirect('EditRoom', assetID)

def createAsset(request):
    template = loader.get_template('InsertAssetSelect.html')
    context = {}
    return HttpResponse(template.render(context, request))



def createService(request, assetID = None):
    ServiceForm = None
    editService_form = None

    if Asset.objects.filter(pk=assetID).exists():
        existingAsset = Asset.objects.get(pk=assetID) 
        editService_form = InsertServiceForm(currentUser=request,initial={
                    'assetName': existingAsset.assetname,
                    'assetQuantity': existingAsset.quantity,
                    'serviceType': Service.objects.get(assetid=assetID).servicetypeid_servicetype.id,
                    'description': Service.objects.get(assetid=assetID).description
        })
        ServiceForm = InsertServiceForm(request.POST, currentUser=request.user)
        if ServiceForm.is_valid():
            newService = ServiceForm.save(assetID)
            return redirect('ViewAssets')       
    else:
        if request.method == 'POST':
            ServiceForm = InsertServiceForm(request.POST, currentUser=request.user)
            if ServiceForm.is_valid():
                newService = ServiceForm.save()
                return redirect('ViewAssets')        
          
        else:
            ServiceForm = InsertServiceForm(currentUser=request.user)

    template = loader.get_template('InsertService.html')
    context = {
        'ServiceForm' : ServiceForm,
        'editService_form' : editService_form
        
    }
    return HttpResponse(template.render(context, request))    

def createEquipment(request, assetID = None):
    errorMessage = None
    EquipmentForm = None
    editEquipmentForm = None

    if Asset.objects.filter(pk=assetID).exists():
        existingAsset = Asset.objects.get(pk=assetID) 
        editEquipmentForm = InsertEquipmentForm(currentUser=request,initial={
                    'assetName': existingAsset.assetname,
                    'assetQuantity': existingAsset.quantity,
                    'equipmentType': Equipment.objects.get(assetid=assetID).equipmenttypeid_equipmenttype.id,
        })
        
        EquipmentForm = InsertEquipmentForm(request.POST, currentUser=request.user)
        if EquipmentForm.is_valid():
            newEquipment = EquipmentForm.save(assetID)   
            return redirect('ViewAssets')                
    else:
        if request.method == 'POST':
            EquipmentForm = InsertEquipmentForm(request.POST, currentUser=request.user)
            if EquipmentForm.is_valid():
                newEquipment = EquipmentForm.save()  
                return redirect('ViewAssets')            
        else:
            EquipmentForm = InsertEquipmentForm(currentUser=request.user)


    template = loader.get_template('InsertEquipment.html')
    context = {
        'errorMessage' : errorMessage,
        'EquipmentForm' : EquipmentForm,
        'editEquipmentForm': editEquipmentForm
        
    }
    return HttpResponse(template.render(context, request))    

def createRoom(request, assetID = None):
    errorMessage = None
    RoomForm = None
    editRoomForm = None
    if Asset.objects.filter(pk=assetID).exists():
        existingAsset = Asset.objects.get(pk=assetID) 
        existingRoom = Rooms.objects.get(assetid=assetID)
        editRoomForm = InsertRoomForm(currentUser=request,initial={
                    'assetName': existingAsset.assetname,
                    'campus': existingRoom.buildingid_building.campusid.campusname,
                    'room_type': existingRoom.room_type.id,
                    'buildings': existingRoom.buildingid_building.id,
                    'capacity': existingRoom.capacity,
                    'capacityRed': existingRoom.reducedMobCapacity
        })
        RoomForm = InsertRoomForm(request.POST, currentUser=request.user)   
        if RoomForm.is_valid():
            newRoom = RoomForm.save(assetID) 
            return redirect('ViewAssets')    
    else:
        if request.method == 'POST':
            RoomForm = InsertRoomForm(request.POST, currentUser=request.user)
            if RoomForm.is_valid():
                newRoom = RoomForm.save()    
                return redirect('ViewAssets')         
        else:
            RoomForm = InsertRoomForm(currentUser=request.user)


    template = loader.get_template('InsertRoom.html')
    context = {
        'errorMessage' : errorMessage,
        'RoomForm' : RoomForm,
        'editRoomForm': editRoomForm
        
    }
    return HttpResponse(template.render(context, request))    

def view_associate_asset(request):
    template = loader.get_template('ViewAssociateAssets.html')
    events = Event.objects.all()

    for event in events:
        if AssetEvent.objects.filter(eventid_event= event.id).exists():
            event.hasAssets = 1
        else:
            event.hasAssets = 0
    context = {
        'events': events,        
    }
    return HttpResponse(template.render(context, request))


def associate_asset(request, eventID = 0, assetID = 0):
         
    existingEvent = Event.objects.get(pk=eventID) 
    asset = Asset.objects.get(pk = assetID)
    Form = None

   
    newAsset_Event = Form.save() 
      

    return redirect('ViewAssetsToAssociate', eventID)         

def consultar_recursos_para_add(request, eventID = 0):
    
    Assets = Asset.objects.all()
    i = 0
    sizeofAssets = len(Assets)
    while i < sizeofAssets :
        if Asset.getServiceType(Assets[i]) is not None:
            Assets[i].subtype =  Asset.getServiceType(Assets[i])
            
        elif Asset.getEquipmentType(Assets[i]) is not None:
            Assets[i].subtype = Asset.getEquipmentType(Assets[i])
            
        elif Asset.getRoom(Assets[i]) is not None:
            room = Asset.getRoom(Assets[i])
            buildingg = Rooms.room_GetBuilding(room)
            
            Assets[i].subtype = Building.CampusName_BuildingName(buildingg)
        i += 1

    template = loader.get_template('ViewAssetsToAssociate.html')
    context = {
        'Assets' : Assets,
        'eventID' : eventID,
    }
    return HttpResponse(template.render(context, request))    

def consultar_recursos_do_evento(request, eventID = 0):

    template = loader.get_template('ViewAssetsOfEvent.html')
    context = {
        'Assets' : AssetEvent.objects.filter(eventid_event=eventID)
    }
    return HttpResponse(template.render(context, request))    