from django import forms
from .models import Asset
import datetime
from pip._vendor.urllib3 import request
from FormManagement.models import Form
from AssetManagement.models import Service, Servicetype

class InsertServiceForm(forms.Form):
	user = None
	assetName = forms.CharField(label='Asset Name', max_length=255, required=False)
	assetQuantity = forms.IntegerField(label='Quantity', required=True)
	
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
