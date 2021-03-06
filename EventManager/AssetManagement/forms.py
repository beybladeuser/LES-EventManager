from django import forms
from .models import Asset
import datetime
from FormManagement.models import Form
from AssetManagement.models import Service, Servicetype, Equipment, Equipmenttype, Campus
from AssetManagement.models import AssetType, Building, RoomType, Rooms
from django.utils.safestring import mark_safe
from PreEventManagement.models import AssetEvent, Event
from django.forms import ModelForm, TextInput, EmailInput

class InsertServiceForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Nome do Serviço', max_length=255, required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	assetQuantity = forms.IntegerField(label='Quantidade', required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	
	OPTIONS_serviceType = Service.makeOptions()
	serviceType =  forms.CharField(widget=forms.Select(choices=OPTIONS_serviceType, attrs={'class' : 'input'}), label='Service Type', required=True)
	description = forms.CharField(label='Descrição',  max_length=255, required=False, widget=forms.TextInput(attrs={'class' : 'input'}))



	def __init__(self, *args, **kwargs):
		if kwargs:
			self.user = kwargs.pop('currentUser', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		if not self.user:
			self.add_error("serviceType", 'Must be logged in to perform this action')
			return
		else:
			assetName = self.cleaned_data.get('assetName')
			assetQuantity = self.cleaned_data.get('assetQuantity')
			serviceType = self.cleaned_data.get('serviceType')
			description = self.cleaned_data.get('description')
		

	def save(self, assetID = None):
		if assetID is not None:
			newAsset = Asset.objects.get(id=assetID)
		else:
			newAsset = Asset()
			newAsset.assettype = AssetType.objects.get(pk=1);
		
		newAsset.assetname = self.cleaned_data.get('assetName')
		newAsset.quantity = self.cleaned_data.get('assetQuantity')
		newAsset.save()

		newService = Service()
		newService.assetid = newAsset
		newService.servicetypeid_servicetype = Servicetype.objects.get(pk=self.cleaned_data.get('serviceType'))
		newService.description = self.cleaned_data.get('description')
		newService.save()
	
	class Meta:
		model = Asset


class InsertEquipmentForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Nome do Equipamento', max_length=255, required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	assetQuantity = forms.IntegerField(label='Quantidade', required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	
	OPTIONS_equipmentType = Equipment.makeOptions()
	equipmentType =  forms.CharField(widget=forms.Select(choices=OPTIONS_equipmentType, attrs={'class' : 'input'}), label='Tipo de Equipamento', required=True)

	def __init__(self, *args, **kwargs):
		if kwargs:
			self.user = kwargs.pop('currentUser', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		if not self.user:
			self.add_error("equipmentType", 'Must be logged in to perform this action')
			return
		else:
			assetName = self.cleaned_data.get('assetName')
			assetQuantity = self.cleaned_data.get('assetQuantity')
			equipmentType = self.cleaned_data.get('equipmentType')
		

	def save(self, assetID = None):
		if assetID is not None:
			newAsset = Asset.objects.get(id=assetID)
		else:
			newAsset = Asset()
			newAsset.assettype = AssetType.objects.get(pk=2);
		
		newAsset.assetname = self.cleaned_data.get('assetName')
		newAsset.quantity = self.cleaned_data.get('assetQuantity')
		newAsset.save()

		newEquipment = Equipment()
		newEquipment.assetid = newAsset
		newEquipment.equipmenttypeid_equipmenttype = Equipmenttype.objects.get(pk=self.cleaned_data.get('equipmentType'))
		newEquipment.save()
	
	
	class Meta:
		model = Asset


class InsertRoomForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Número/Nome do Espaço', max_length=255, required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
		
	OPTIONS_campus = Campus.makeOptions()
	campus =  forms.CharField(widget=forms.Select(choices=OPTIONS_campus, attrs={'class' : 'input'}), label='Campus', required=True)

	OPTIONS_Rooms = Rooms.makeOptions()
	room_type =  forms.CharField(widget=forms.Select(choices=OPTIONS_Rooms, attrs={'class' : 'input'}), label='Tipo de Espaço', required=True)

	
	OPTIONS_buildings = Building.makeOptions()
	buildings =  forms.CharField(widget=forms.Select(choices=OPTIONS_buildings, attrs={'class' : 'input'}), label='Edifício', required=True)

	capacity = forms.IntegerField(label='Capacidade', required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	capacityRed = forms.IntegerField(label='Lugares de cap. reduzida', required=True, widget=forms.TextInput(attrs={'class' : 'input'}))



	def __init__(self, *args, **kwargs):
		if kwargs:
			self.user = kwargs.pop('currentUser', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		if not self.user:
			self.add_error("equipmentType", 'Must be logged in to perform this action')
			return
		else:
			assetName = self.cleaned_data.get('assetName')
			campus = self.cleaned_data.get('campus')
			room_type = self.cleaned_data.get('room_type')
			buildings = self.cleaned_data.get('buildings')
			capacity = self.cleaned_data.get('capacity')
			capacityRed = self.cleaned_data.get('capacityRed')
			
		

	def save(self, assetID = None):
		if assetID is not None:
			newAsset = Asset.objects.get(id=assetID)
		else:
			newAsset = Asset()
			newAsset.assettype = AssetType.objects.get(pk=3);
		newAsset.assetname = self.cleaned_data.get('assetName')
		newAsset.quantity = 1
		newAsset.save()

		newRoom = Rooms()
		newRoom.assetid = newAsset
		newRoom.room_type = RoomType.objects.get(pk=self.cleaned_data.get('room_type'))
		newRoom.buildingid_building = Building.objects.get(pk=self.cleaned_data.get('buildings'))
		newRoom.capacity = self.cleaned_data.get('capacity')
		newRoom.reducedMobCapacity = self.cleaned_data.get('capacityRed')
		newRoom.save()
	

	class Meta:
		model = Asset


class AssociateAssetForm(forms.Form):
	user = None
	OPTIONS_event = Event.makeOptions()
	event =  forms.CharField(widget=forms.Select(choices=OPTIONS_event, attrs={'class' : 'input'}), label='Evento', required=True)
	
	OPTIONS_assetToAssociate = Asset.makeOptions()
	assetToAssociate = forms.CharField(widget=forms.Select(choices=OPTIONS_assetToAssociate, attrs={'class' : 'input'}), label='Recurso', required=True)

	

	def __init__(self, *args, **kwargs):
		if kwargs:
			self.user = kwargs.pop('currentUser', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):
		if not self.user:
			self.add_error("equipmentType", 'Must be logged in to perform this action')
			return
		else:
			eventName = self.cleaned_data.get('event')
			assetToAssociate = self.cleaned_data.get('assetToAssociate')
		
			

	def save(self):
	
		newAsset_Event = AssetEvent()
		newAsset_Event.eventid_event = Event.objects.get(pk=self.cleaned_data.get('event'))
		newAsset_Event.assetid_asset = Asset.objects.get(pk=self.cleaned_data.get('assetToAssociate'))
		newAsset_Event.save()
	

	class Meta:
		model = Asset

