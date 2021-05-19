#rom django import forms
#rom .models import Asset
#mport datetime
#rom pip._vendor.urllib3 import request
#rom FormManagement.models import Form
#
#
#lass InsertAssetForm(forms.Form):
#	user = None
#	assetName = forms.CharField(label='Asset Name', max_length=255, required=False)
#	assetQuantity = forms.IntegerField(label='Quantity', required=True)
#	OPTIONS_assetType = assettype.makeOptions()
#	assetType = 
#
#	class Meta:
#		model = Asset
#
#
#
#
#
#
#	def __init__(self, *args, **kwargs):
#		if kwargs:
#			self.user = kwargs.pop('currentUser', None)
#		super().__init__(*args, **kwargs)
#
#
#
#
#	def clean(self, *args, **kwargs):
#		if not self.user:
#			return
#		else:
#			assetName = self.cleaned_data.get('assetName')
#			assetQuantity = self.cleaned_data.get('assetQuantity')
#		
#		
#
#	def save(self):
#       form = insert_assets(request.POST)
#       if form.isvalid():
#           form.save()
#       else:
#           form.save()