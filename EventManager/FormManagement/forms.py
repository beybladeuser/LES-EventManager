from django import forms
from .models import Formtype, Form, Answer, Multipleoptions
from PreEventManagement.models import Eventtype
from EventManagement.models import Resgistration
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


#para inicializar este form este deve estar na forma "form = EventManagerForm(eventManagerFormID=<formID>, associatedRegistration=<resID>, associatedEvent=<EvID>)"
#onde <formID> é o ID do form a responder, <resID> e o ID de qual registo de inscricao as respostas vao ficar associadas
#e <EvID> e o ID de qual evento as respostas vao ficar associadas
#atencao so um dos dois valores de <EvID> e <resID> e que pode estar definido ou seja so e possivel declarar este form de uma das 2 maneiras
#"form = EventManagerForm(eventManagerFormID=<formID>, associatedRegistration=<resID>, associatedEvent=None)"
#"form = EventManagerForm(eventManagerFormID=<formID>, associatedRegistration=None, associatedEvent=<EvID>)"
#todos os IDs devem existir
class EventManagerForm(forms.Form) :
	form = None
	registration = None
	event = None
	hasError = False
	def __init__(self, *args, **kwargs):
		formID = None
		
		if kwargs :
			formID = kwargs.pop('eventManagerFormID', None)
			registrationID = kwargs.pop('associatedRegistration', None)
			eventID = kwargs.pop('associatedEvent', None)
		super().__init__(*args, **kwargs)
		
		
		if formID and Form.objects.filter(pk=formID).exists():
			self.form = Form.objects.get(pk=formID)
			for question in self.form.formquestions :
				if question.questiontypeid_questiontype.id == 1 :
					self.fields["question"+str(question.id)] = forms.CharField(required=question.required, label=question.question)
				elif question.questiontypeid_questiontype.id == 2 :
					self.fields["question"+str(question.id)] = forms.ChoiceField(widget=forms.RadioSelect,choices=question.makeOptions(), label=question.question, required=question.required)
		else :
			self.hasError = True

		if registrationID and Resgistration.objects.filter(pk=registrationID).exists():
			self.registration = Resgistration.objects.get(pk=registrationID)

		if eventID and Event.objects.filter(pk=eventID).exists():
			self.event = Event.objects.get(pk=eventID)

		if (self.registration and self.event) or (not self.registration and not self.event) :
			self.hasError

	def save(self) :
		if self.hasError :
			return None
		for question in self.form.formquestions :
			if self.cleaned_data["question"+str(question.id)] :
				answer = self.cleaned_data["question"+str(question.id)]
				
				answerModel = Answer()
				answerModel.questionsid_questions = question
				if self.event:
					answerModel.eventid_event = self.event
				elif self.registration:
					answerModel.resgistrationid = self.registration
				else :
					return None
				
				answerModel.dateofcreation = datetime.datetime.now()
				if question.questiontypeid_questiontype.id == 1 :
					answerModel.answer = answer
				elif question.questiontypeid_questiontype.id == 2 :
					answerModel.answer = Multipleoptions.objects.get(pk=answer[0]).option
				
				answerModel.save()
		
		return self.form
