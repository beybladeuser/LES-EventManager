from django import forms
from .models import Asset
import datetime
from pip._vendor.urllib3 import request
from FormManagement.models import Form
from AssetManagement.models import Service, Servicetype, Equipment, Equipmenttype, Campus
from AssetManagement.models import Building, Rooms


class InsertServiceForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Nome do Serviço', max_length=255, required=False)
	assetQuantity = forms.IntegerField(label='Quantidade', required=True)
	
	OPTIONS_serviceType = Service.makeOptions()
	serviceType =  forms.CharField(widget=forms.Select(choices=OPTIONS_serviceType, attrs={'class' : 'input'}), label='Service Type', required=True)

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
		

	def save(self):
		newAsset = Asset()
		newAsset.assetname = self.cleaned_data.get('assetName')
		newAsset.quantity = self.cleaned_data.get('assetQuantity')
		newAsset.save()

		newService = Service()
		newService.assetid = newAsset
		newService.servicetypeid_servicetype = Servicetype.objects.get(pk=self.cleaned_data.get('serviceType'))
		newService.save()
	class Meta:
		model = Asset


class InsertEquipmentForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Nome do Equipamento', max_length=255, required=False)
	assetQuantity = forms.IntegerField(label='Quantidade', required=True)
	
	OPTIONS_equipmentType = Equipment.makeOptions()
	equipmentType =  forms.CharField(widget=forms.Select(choices=OPTIONS_equipmentType, attrs={'class' : 'input'}), label='Equipment Type', required=True)

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
		

	def save(self):
		newAsset = Asset()
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
	assetName = forms.CharField(label='Número/nome da Sala/Anf.', max_length=255, required=False)
		
	OPTIONS_campus = Campus.makeOptions()
	campus =  forms.CharField(widget=forms.Select(choices=OPTIONS_campus, attrs={'class' : 'input'}), label='Campus', required=True)

	OPTIONS_buildings = Building.makeOptions()
	buildings =  forms.CharField(widget=forms.Select(choices=OPTIONS_buildings, attrs={'class' : 'input'}), label='Edifício', required=True)

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
			buildings = self.cleaned_data.get('buildings')
			
		

	def save(self):
		newAsset = Asset()
		newAsset.assetname = self.cleaned_data.get('assetName')
		newAsset.quantity = 1
		newAsset.save()

		newRoom = Rooms()
		newRoom.assetid = newAsset
	
		newRoom.buildingid_building = Building.objects.get(pk=self.cleaned_data.get('buildings'))
		newRoom.save()
	

	class Meta:
		model = Asset
