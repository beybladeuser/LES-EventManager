from django import forms
from .models import Formtype, Form, Answer, Multipleoptions, Questiontype, Questions, QuestionsForm
from PreEventManagement.models import Eventtype
from EventManagement.models import Resgistration
import datetime
from django.utils.safestring import mark_safe

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
			self.registration = kwargs.pop('associatedRegistration', None)
			self.event = kwargs.pop('associatedEvent', None)
		super().__init__(*args, **kwargs)
		
		
		if formID and Form.objects.filter(pk=formID).exists():
			self.form = Form.objects.get(pk=formID)
			for question in self.form.formquestions :
				if question.questiontypeid_questiontype.id == 1 :
					self.fields["question"+str(question.id)] = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input'}),required=question.required, label=question.question)
				elif question.questiontypeid_questiontype.id == 2 :
					self.fields["question"+str(question.id)] = forms.ChoiceField(widget=forms.RadioSelect,choices=question.makeOptions(), label=question.question, required=question.required)
		else :
			self.hasError = True

		if (self.registration and self.event) or (not self.registration and not self.event) :
			self.hasError = True

	def clean(self) :
		if self.hasError :
			self.add_error(self.form.formquestions[0].question, 'Only one of the init args: associatedRegistration or associatedEvent can be passed as a non null value')
			return None
		for question in self.form.formquestions :
			field_name = "question"+str(question.id)
			if self.cleaned_data[field_name] :
				if self.event and question.getAnswersForForm(self.form.id).filter(eventid_event=self.event.id).exists() :
					self.add_error(field_name, 'Cant Answer to this form twice')
				elif self.registration and question.getAnswersForForm(self.form.id).filter(resgistrationid=self.registration.id).exists() :
					self.add_error(field_name, 'Cant Answer to this form twice')



	def save(self) :
		for question in self.form.formquestions :
			if self.cleaned_data["question"+str(question.id)] :
				answer = self.cleaned_data["question"+str(question.id)]
				
				answerModel = Answer()
				answerModel.questionsid_questions = question
				answerModel.associatedformid = self.form
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
					answerModel.answer = Multipleoptions.objects.get(pk=answer).option
				
				answerModel.save()
		
		return self.form
