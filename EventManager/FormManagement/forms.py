from django import forms
from .models import Formtype, Form, Answer, Multipleoptions, Questiontype, Questions, QuestionsForm
from PreEventManagement.models import Eventtype
from EventManagement.models import Resgistration
import datetime
from django.utils.safestring import mark_safe

# Create your forms here.

class formCreation(forms.Form):
	user = None
	formId = forms.CharField(widget=forms.HiddenInput, max_length=255, required=False)
	formName = forms.CharField(label='Nome do Formulário', max_length=255, required=True, widget=forms.TextInput(attrs={'class' : 'input'}))
	OPTIONS_eventType = Eventtype.makeOptions()
	eventType = forms.CharField(widget=forms.Select(choices=OPTIONS_eventType, attrs={'class' : 'input'}), label='Tipo de evento', required=True)

	def __init__(self, *args, **kwargs):
		if kwargs :
			self.user = kwargs.pop('currentUser', None)
		super().__init__(*args, **kwargs)
		OPTIONS_formType = Formtype.makeOptions(self.user)
		self.fields["formType"] = forms.CharField(widget=forms.Select(choices=OPTIONS_formType, attrs={'class' : 'input'}), label='Tipo de formulário', required=True)

	class Meta:
		model = Formtype

	def clean(self, *args, **kwargs):

		formId = self.cleaned_data.get("formId")
		if not self.user :
			self.add_error("eventType", 'É necessário possuir a sessão iniciada para concluir esta ação')
			return
		
		if formId and Form.objects.filter(id=formId).exists():
			form = Form.objects.get(id=formId)
			if not form.canEdit(self.user) :
				self.add_error("eventType", 'Não pode editar este formulário')
				return

		formType = self.cleaned_data.get("formType")
		formName = self.cleaned_data.get("formName")
		if not formId :
			if Form.objects.filter(formname=formName, formtypeid_formtype=formType, archived=False).exists() :
				self.add_error("formName", 'Impossível criar formulários com nomes duplicados')
		else :
			if Form.objects.filter(formname=formName, formtypeid_formtype=formType, archived=False).exclude(id=formId).exists() :
				self.add_error("formName", 'Impossível criar formulários com nomes duplicados')
		
		if not Formtype.objects.get(pk=formType).canCreate(self.user) :
			self.add_error("formType", 'Não pode criar eventos do tipo especificado')


	def clean_eventType(self, *args, **kwargs):
		formType = self.cleaned_data.get("formType")
		eventType = self.cleaned_data.get("eventType")
		formId = self.cleaned_data.get("formId")
		temp = Form.objects.filter(eventtypeid=eventType, formtypeid_formtype=formType, archived=False)
		if not formId:
			if formType == "1" and temp.exists() :
				raise forms.ValidationError("Não é possivel ter dois formulários de proposta não arquivados do mesmo tipo de evento")
			else:
				return eventType
		else:
			if formType == "1" and temp.exclude(id=formId).exists() :
				raise forms.ValidationError("Não é possivel ter dois formulários de proposta não arquivados do mesmo tipo de evento")
			else:
				return eventType

	def save(self, FormID = None):
		if FormID and Form.objects.filter(id=FormID).exists():
			newForm = Form.objects.get(pk=FormID)
			isEdit = True
		else :
			newForm = Form()
			isEdit = False
		wasChanged = False
		if not isEdit or newForm.formname != self.cleaned_data['formName'] :
			newForm.formname = self.cleaned_data['formName']
			wasChanged = True
		
		
		if not isEdit or newForm.formtypeid_formtype.id == self.cleaned_data['formType'] :
			formType = Formtype.objects.get(pk=self.cleaned_data['formType'])
			newForm.formtypeid_formtype = formType
			wasChanged = True

		if not isEdit or newForm.eventtypeid.id == self.cleaned_data['eventType'] :
			eventType = Eventtype.objects.get(pk=self.cleaned_data['eventType'])
			newForm.eventtypeid = eventType
			wasChanged = True

		if not FormID :
			newForm.dateofcreation = datetime.datetime.now()

		if wasChanged :
			newForm.dateoflastedit = datetime.datetime.now()

		if not FormID :
			newForm.createdby = self.user
		
		if wasChanged :
			newForm.lasteditedby = self.user
			newForm.save()
		return newForm


class openEndedQuestionCreation(forms.Form):
	user = None
	form = None
	questionToEdit = None
	question = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input'}), label='Question', max_length=255, required=True)
	OPTIONS_questionType = Questiontype.makeOptions()
	questionType = forms.CharField(widget=forms.Select(choices=OPTIONS_questionType, attrs={'class' : 'input', "onChange":'checkType()'}), label='Tipo de evento', required=True)
	options = ((True, 'Sim'), (False, 'Não'))
	required = forms.ChoiceField(widget=forms.RadioSelect,choices=options, label="É Requerida", required=True)

	def __init__(self, *args, **kwargs):
		if kwargs :
			self.user = kwargs.pop('currentUser', None)
			self.form = kwargs.pop('associatedForm', None)
			self.questionToEdit = kwargs.pop('questionToEdit', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):

		if not self.user :
			self.add_error("question", 'É necessário possuir a sessão iniciada para concluir esta ação')
			return
		
		if self.questionToEdit and not self.questionToEdit.canEdit(self.user):
			self.add_error("question", 'Não pode editar esta questão')
			return

		question = self.cleaned_data.get("question")
		if self.questionToEdit :
			if Questions.objects.filter(question=question).exclude(id=self.questionToEdit.id).exists() :
				self.add_error("question", 'Não é possivel criar questões duplicadas')
		else :
			if Questions.objects.filter(question=question).exists() :
				self.add_error("question", 'Não é possivel criar questões duplicadas')

	def save(self) :
		newQuestion = None
		if self.questionToEdit :
			newQuestion = self.questionToEdit
		else :
			newQuestion = Questions()

		wasChanged = False
		question = self.cleaned_data.get("question")
		if not self.questionToEdit or self.questionToEdit.question != question :
			newQuestion.question = question
			wasChanged = True
		
		if not self.questionToEdit :
			newQuestion.questiontypeid_questiontype = Questiontype.objects.get(id=1)
			wasChanged = True

		required = self.cleaned_data.get("required")
		if not self.questionToEdit or self.questionToEdit.required != required :
			newQuestion.required = required
			wasChanged = True

		if not self.questionToEdit :
			newQuestion.createdby = self.user
			newQuestion.dateofcreation = datetime.datetime.now()
		
		if wasChanged :
			newQuestion.lasteditedby = self.user
			newQuestion.dateoflastedit = datetime.datetime.now()
	
			newQuestion.save()

		if self.form :
			self.form.associateQuestion(newQuestion, self.user)

		return newQuestion



class QuestionOptionForm(forms.Form):
	user = None
	associatedQuestion = None
	optionToEdit = None
	option = forms.CharField(widget=forms.TextInput(attrs={'class' : 'input'}),label='Opção', max_length=255, required=True)

	def __init__(self, *args, **kwargs):
		if kwargs :
			self.user = kwargs.pop('currentUser', None)
			self.associatedQuestion = kwargs.pop('associatedQuestion', None)
			self.optionToEdit = kwargs.pop('optionToEdit', None)
		super().__init__(*args, **kwargs)

	def clean(self, *args, **kwargs) :
		if not self.associatedQuestion.canEdit(self.user) :
			self.add_error("option", 'Não pode editar esta questão')
			return
		
		if self.optionToEdit and self.optionToEdit.questionsid_questions != self.associatedQuestion :
			self.add_error("option", 'Opção a editar não está relacionada com a questão dada')
	
	def save(self) :
		newOption = None
		if self.optionToEdit :
			newOption = self.optionToEdit
		else :
			newOption = Multipleoptions()

		newOption.option = self.cleaned_data.get("option")
		if not self.optionToEdit :
			newOption.questionsid_questions = self.associatedQuestion

		newOption.save()

		self.associatedQuestion.notifyNewOption(self.user)

		return newOption

		


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
					self.fields["question"+str(question.id)] = forms.CharField(required=question.required, label=question.question)
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
					answerModel.answer = Multipleoptions.objects.get(pk=answer[0]).option
				
				answerModel.save()
		
		return self.form
