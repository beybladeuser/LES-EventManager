from django import forms
from .models import Formtype, Form
from Models.models import Eventtype
import datetime


# Create your forms here.

class formCreation(forms.Form):
	formId = forms.CharField(widget=forms.HiddenInput, max_length=255, required=False)
	formName = forms.CharField(label='Form Name', max_length=255, required=True)
	OPTIONS_formType = Formtype.makeOptions()
	formType = forms.CharField(widget=forms.Select(choices=OPTIONS_formType), label='Form Type', required=True)
	OPTIONS_eventType = Eventtype.makeOptions()
	eventType = forms.CharField(widget=forms.Select(choices=OPTIONS_eventType), label='Event Type', required=True)

	class Meta:
		model = Formtype

	def clean_eventType(self, *args, **kwargs):
		formType = self.cleaned_data.get("formType")
		eventType = self.cleaned_data.get("eventType")
		formId = self.cleaned_data.get("formId")

		temp = Form.objects.filter(eventtypeid=eventType, formtypeid_formtype=formType)
		if not formId:
			if formType == "1" and temp.exists() :
				raise forms.ValidationError("Cannot have two proposal forms for the same event type")
			else:
				return eventType
		else:
			if formType == "1" and temp.exclude(id=formID).exists() :
				raise forms.ValidationError("Cannot have two proposal forms for the same event type")
			else:
				return eventType

		


	def save(self, FormID = None, user = None):
		if FormID and Form.objects.filter(id=FormID).exists():
			newForm = Form.objects.get(pk=FormID)
		else :
			newForm = Form()
		
		newForm.formname = self.cleaned_data['formName']

		formType = Formtype.objects.get(pk=self.cleaned_data['formType'])
		newForm.formtypeid_formtype = formType

		eventType = Eventtype.objects.get(pk=self.cleaned_data['eventType'])
		newForm.eventtypeid = eventType

		if not FormID :
			newForm.dateofcreation = datetime.datetime.now()

		newForm.dateoflastedit = datetime.datetime.now()

		if not FormID :
			newForm.createdby = user
		
		newForm.lasteditedby = user
		

		newForm.save()
		return newForm