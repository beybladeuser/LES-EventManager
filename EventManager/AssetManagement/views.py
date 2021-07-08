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
            
            Assets[i].subtype = Asset.getRoom(Assets[i]).room_type
            Assets[i].room = room
            Assets[i].building = buildingg



        if AssetEvent.objects.filter(assetid_asset=Assets[i].id).exists():
            Assets[i].isAssociated = AssetEvent.objects.filter(assetid_asset=Assets[i].id, isAssociated=True).exists()
        
        i += 1

    context = {
        'assetTypes': AssetType.getTypes(),
        'equipmentTypes': Equipmenttype.getEquipmenttypes(),
        'serviceTypes': Service.makeOptions(),
        'roomTypes': RoomType.getRoomTypes(),
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
    AssetsAssociated = AssetEvent.objects.filter(assetid_asset=assetID)
    for assetAssociated in AssetsAssociated:
        assetAssociated.delete()

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
        'isViewAssets': 0,   
    }
    return HttpResponse(template.render(context, request))


def associate_asset(request, eventID = 0, assetID = 0):
         
    existingEvent = Event.objects.get(pk=eventID) 
    asset = Asset.objects.get(pk = assetID)

    AssetEvent_ = AssetEvent()
    AssetEvent_.eventid_event = Event.objects.get(pk=eventID)
    AssetEvent_.assetid_asset = Asset.objects.get(pk=assetID)
    AssetEvent_.isAssociated = True
    AssetEvent_.save()

    return redirect('ViewAssetsOfEvent', eventID) 

def associate_assetV2(request, assocID = None):
    temp = None
    if assocID :
        if AssetEvent.objects.filter(pk = assocID).exists() :
            temp = AssetEvent.objects.get(pk = assocID)
            temp.isAssociated = True
            temp.save()
    if temp :
        return redirect('ViewAssetsOfEvent', temp.eventid_event.id)
    return redirect('homepage')     

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
        'assetTypes': AssetType.getTypes(),
        'equipmentTypes': Equipmenttype.getEquipmenttypes(),
        'serviceTypes': Service.makeOptions(),
        'roomTypes': RoomType.getRoomTypes(),
        'Assets' : Assets,
        'eventID' : eventID,
        'isViewAssets': 0,
        'eventName': Event.objects.get(pk=eventID).eventname
    }
    return HttpResponse(template.render(context, request))    

def consultar_recursos_do_evento(request, eventID = 0):

    template = loader.get_template('ViewAssetsOfEvent.html')
    AssetsEvent = AssetEvent.objects.filter(eventid_event=eventID)
    
    if AssetsEvent is not None:
        i = 0;
        size = len(AssetsEvent)
        while i < size:
            asset = Asset.objects.get(pk=AssetsEvent[i].assetid_asset.id)
            if Asset.getServiceType(asset) is not None:
                AssetsEvent[i].assetid_asset.subtype =  Asset.getServiceType(asset)
                
            elif Asset.getEquipmentType(asset) is not None:
                AssetsEvent[i].assetid_asset.subtype = Asset.getEquipmentType(asset)
                
            elif Asset.getRoom(asset) is not None:
                room = Asset.getRoom(asset)
                buildingg = Rooms.room_GetBuilding(room)
                AssetsEvent[i].assetid_asset.subtype = Building.CampusName_BuildingName(buildingg)
            
            i+=1
        
    context = {
        'assetTypes': AssetType.getTypes(),
        'equipmentTypes': Equipmenttype.getEquipmenttypes(),
        'serviceTypes': Service.makeOptions(),
        'roomTypes': RoomType.getRoomTypes(),
        'Assets' : AssetsEvent,
        'assetTypes' : AssetType.getTypes(),
        'isViewAssets': 1,
        'eventName': Event.objects.get(pk=eventID).eventname,
        'eventID':eventID,
    }
    return HttpResponse(template.render(context, request))    

def desassociar_recurso(request, eventID = 0 , assetID = 0):

    assetevent = AssetEvent.objects.filter(eventid_event=eventID, assetid_asset=assetID).order_by('eventid_event')[0]
    assetevent.delete() 
    return redirect('ViewAssetsOfEvent', eventID)


def detalhes(request, assetID = 0):
    template = loader.get_template('detalhes.html')
    
    asset = Asset.objects.get(pk=assetID)
    isType = 0
    if asset.assettype.id is 1:    # Serviço
        service = Service.objects.get(pk = assetID)
        asset.subtype = service.servicetypeid_servicetype.typename
        asset.description = service.description
        isType = 1
 
    elif asset.assettype.id is 2:   # Equipamento
        equipment = Equipment.objects.get(pk=assetID)
        asset.subtype = equipment.equipmenttypeid_equipmenttype.typename
        isType = 2

    elif asset.assettype.id is 3:    # Espaço
        room = Rooms.objects.get(pk=assetID)
        asset.subtype = room.room_type.typename
        asset.building = room.buildingid_building.buildingname
        asset.campus = room.buildingid_building.campusid.campusname
        asset.capacity = room.capacity
        asset.reducedMobCapacity = room.reducedMobCapacity
        
        isType = 3
    
    context = {
        'asset': asset,
        'istype': isType,
    }
    return HttpResponse(template.render(context, request))    