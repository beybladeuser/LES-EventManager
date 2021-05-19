from django import forms
from .models import Asset
import datetime


class InsertAssetForm(forms.Form):
	assetName = forms.CharField(label='Asset Name', max_length=255, required=False)
	assetQuantity = forms.IntegerField(label='Quantity', required=True)
