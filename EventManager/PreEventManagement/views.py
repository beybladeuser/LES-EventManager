from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from PreEventManagement.models import *
from AssetManagement.models import *
from FormManagement.models import *
from EventManagement.models import *

#	proposal_form_type = Formtype.objects.get(typename="Proposal")
#
#	event_types = Eventtype.objects.all()
#	for event_type in event_types:
#		if Form.objects.filter(eventtypeid=event_type, formtypeid_formtype=proposal_form_type).count() == 0:
#			raise Exception("No proposal form exists for event type " + event_type.typename)

def index(request):
	template = loader.get_template('homePreEvent.html')
	context = {}
	return HttpResponse(template.render(context, request))




def validate(request, id):
	event = Event.objects.get(id=id)
	event.wasvalidated = '1'
	event.save()
	return redirect("list")


def delete(request, id):
	event = Event.objects.get(id=id)

	Answer.objects.filter(associatedformid=event.formproposalid, eventid_event=event).delete()
	Answer.objects.filter(associatedformid=event.formlogisticsid, eventid_event=event).delete()
	event.delete()
	return redirect("list")




def enroll(request, id):
	event = Event.objects.get(id=id)

	reg = Resgistration(
		eventid_event=event,
		dateofregistration=datetime.datetime.now(),
		waspresent=False,
		participantuserid=request.user
	)
	reg.save()
	return redirect("list")






def ziplist(list1, list2): return [[i, j] for i, j in zip(list1,list2)]
class CreationForm:

	def __initvars(self):
		self.inputs = [
			{#0
				'name': 'eventname',
				'type': 'open',
				'value': None
			},
			{#1
				'name': 'eventcampus',
				'type': 'dropdown',
				'choices': ziplist(
					[x.id for x in Campus.objects.all()],
					[x.campusname for x in Campus.objects.all()]
				),
				'value': None
			},
			{#2
				'name': 'eventtype',
				'type': 'dropdown',
				'choices': ziplist(
					[x.id for x in Eventtype.objects.all()],
					[x.typename for x in Eventtype.objects.all()]
				),
				'controls': 'proposalform',
				'value': None
			},
			{#3
				'name': 'proposalform',
				'type': 'eachform',
				'array': {}
			},
			{#4
				'name': 'logisticsform',
				'type': 'eachform',
				'array': {}
			}
		]

	def __init__(self, request=None):
		self.__initvars()

		proposal_form_type = Formtype.objects.get(id=1)
		proposal_forms = Form.objects.filter(formtypeid_formtype=proposal_form_type, archived=False)

		logistics_form_type = Formtype.objects.get(id=4)
		logistics_forms = Form.objects.filter(formtypeid_formtype=logistics_form_type, archived=False)


		for form in proposal_forms:
			self.inputs[3]['array'][form.eventtypeid.id] = {
				'name': 'proposalform_'+str(form.eventtypeid.id),

				'eventtype': form.eventtypeid.id,
				'formid': form.id,

				'questions': self.__build_form("proposalform", form)
			}
		for form in logistics_forms:
			self.inputs[4]['array'][form.eventtypeid.id] = {
				'name': 'logisticsform_'+str(form.eventtypeid.id),

				'eventtype': form.eventtypeid.id,
				'formid': form.id,

				'questions': self.__build_form("logisticsform", form)
			}

		if request != None:
			self.inputs[0]["value"] = request.POST.get(self.inputs[0]["name"])
			self.inputs[1]["value"] = request.POST.get(self.inputs[1]["name"])
			self.inputs[2]["value"] = request.POST.get(self.inputs[2]["name"])
			for eachform in self.inputs[3]["array"].values():
				for eachquestion in eachform['questions'].values():
					eachquestion["value"] = request.POST.get(eachquestion["name"])
			for eachform in self.inputs[4]["array"].values():
				for eachquestion in eachform["questions"].values():
					eachquestion["value"] = request.POST.get(eachquestion["name"])



	def __build_form(self, generic_name, form):

		registration_form_type = Formtype.objects.get(id=2)
		feedback_form_type = Formtype.objects.get(id=3)


		questions = {}
		for currquestion in form.getQuestions():
			question = {
				'name': generic_name+'_'+ str(form.id)+'_'+str(currquestion.id),
				'question_obj': currquestion,
				'identifier': currquestion.question,
				'required': currquestion.required,
				'type': 'open' if currquestion.questiontypeid_questiontype.id == 1 else 'dropdown',
				'value': None
			}
			if currquestion.questiontypeid_questiontype.id == 2: #options
				question['choices'] = ziplist(
					[option.id for option in currquestion.options],
					[option.option for option in currquestion.options]
				)
			elif currquestion.questiontypeid_questiontype.id == 3: #registration form
				registration_forms = Form.objects.filter(eventtypeid=form.eventtypeid, formtypeid_formtype=registration_form_type, archived=False)
				question['choices'] = ziplist(
					[regform.id for regform in registration_forms],
					[regform.formname for regform in registration_forms]
				)
			elif currquestion.questiontypeid_questiontype.id == 4: #feedback form
				feedback_forms = Form.objects.filter(eventtypeid=form.eventtypeid, formtypeid_formtype=feedback_form_type, archived=False)
				question['choices'] = ziplist(
					[feedbform.id for feedbform in feedback_forms],
					[feedbform.formname for feedbform in feedback_forms]
				)
				print("AAAA: " + str(len(feedback_forms)))

			questions[currquestion.id] = question

		return questions


def create(request):




	if request.method != "POST":
		formboi = CreationForm()
		template = loader.get_template('create_new.html')

		context = {
			'form': formboi.inputs,
			'eventtypes': Eventtype.objects.all()
		}

		print("WHYYYYYYY: " + str(formboi.inputs[2]["value"]))
		return HttpResponse(template.render(context, request))
	else:
		formboi = CreationForm(request)
		#form_name = request.POST['name']
		#form_campus = Campus.objects.get(id=request.POST['campus'])
		#form = Form.objects.get(id=request.POST['form_id'])



		proposal_form_type = Formtype.objects.get(id=1)
		logistic_form_type = Formtype.objects.get(id=4)

		name = formboi.inputs[0]["value"]
		campus = Campus.objects.get(id=int(formboi.inputs[1]["value"]))

		event_type = Eventtype.objects.get(id=int(formboi.inputs[2]["value"]))
		proposal_form = Form.objects.filter(formtypeid_formtype=proposal_form_type, eventtypeid=event_type, archived=False)[0]
		logistic_form = Form.objects.filter(formtypeid_formtype=logistic_form_type, eventtypeid=event_type, archived=False)[0]

		proposal_answers = formboi.inputs[3]["array"][event_type.id]["questions"].values()
		logistic_answers = formboi.inputs[4]["array"][event_type.id]["questions"].values()


		ev = Event(
			eventtypeid=event_type, 
			formresgistrationid=proposal_form,	#dummy
			formfeedbackid=proposal_form,		#dummy
			campusid=campus,
			wasvalidated="0",
			proponentid=request.user,
			eventname=name,
			formproposalid=proposal_form,
			formlogisticsid=logistic_form
		)
		ev.save()

		for answer in proposal_answers:
			if(answer["value"] == ''):
				continue

			an = Answer(
				associatedformid=proposal_form,
				questionsid_questions=answer["question_obj"],
				eventid_event=ev,
				answer=answer["value"],
				dateofcreation=datetime.datetime.now()
			)
			an.save()

		for answer in logistic_answers:

			if(answer["value"] == ''):
				continue

			an = Answer(
				associatedformid=logistic_form,
				questionsid_questions=answer["question_obj"],
				eventid_event=ev,
				answer=answer["value"],
				dateofcreation=datetime.datetime.now()
			)
			an.save()
			
		return redirect("list")







def list(request):
	proposal_form_type = Formtype.objects.get(id=1)
	events = Event.objects.all()
	for event in events:
		try:
			proposal_form = event.formproposalid
			logistic_form = event.formlogisticsid
		except:
			raise Exception("An event (" + event.eventname + ") was created but there is no proposal form for it's type (or there are more than one).")

		proposal_form_questions = proposal_form.getQuestions()
		logistic_form_questions = logistic_form.getQuestions()
		if len(proposal_form_questions) == 0:
			raise Exception("Event type (" + event.eventtypeid.typename + ") proposal form with no questions")
		if len(logistic_form_questions) == 0:
			raise Exception("Event type (" + event.eventtypeid.typename + ") logistics form with no questions")

		event.hasParticipants = Resgistration.objects.filter(eventid_event=event).count() > 0
		event.currently_enrolled = Resgistration.objects.filter(eventid_event=event, participantuserid=request.user).count() > 0

		event.proposal_QAs = []
		for question in proposal_form_questions:
			try:
				answer = Answer.objects.get(eventid_event=event, questionsid_questions=question, associatedformid=proposal_form)
			except:
				if question.required:
					raise Exception("An event was created (" + event.eventname + ") but a question on it's proposal form (" + question.question + ") lacks an answer")
				else:
					print("NOT NEEDED")
					continue

			QA = {
				"question": question,
				"answer": answer
			}
			QA["answer"].has_text = False
			if(QA["question"].questiontypeid_questiontype.id == 2):
				QA["answer"].has_text = True
				QA["answer"].text = Multipleoptions.objects.get(id=int(answer.answer)).option
			elif(QA["question"].questiontypeid_questiontype.id > 2):
				QA["answer"].has_text = True
				QA["answer"].text = Form.objects.get(id=int(answer.answer)).formname

			event.proposal_QAs.append(QA)
		

		event.logistic_QAs = []
		for question in logistic_form_questions:
			try:
				answer = Answer.objects.get(eventid_event=event, questionsid_questions=question, associatedformid=logistic_form)
			except:
				if question.required:
					raise Exception("An event was created (" + event.eventname + ") but a question on it's logistics form (" + question.question + ") lacks an answer")
				else:
					print("NOT NEEDED")
					continue

			QA = {
				"question": question,
				"answer": answer
			}
			QA["answer"].has_text = False
			if(QA["question"].questiontypeid_questiontype.id == 2):
				QA["answer"].has_text = True
				QA["answer"].text = Multipleoptions.objects.get(id=int(answer.answer)).option
			elif(QA["question"].questiontypeid_questiontype.id > 2):
				QA["answer"].has_text = True
				QA["answer"].text = Form.objects.get(id=int(answer.answer)).formname

			event.logistic_QAs.append(QA)


	template = loader.get_template('listEvent_new.html')
	context = {
		'filterKey': '00',
		'eventTypes': Eventtype.objects.all(),
		'campuses': Campus.objects.all(),
		'eventes': events,
		'user': request.user
	}

	return HttpResponse(template.render(context, request))








def edit(request, id):

	event = Event.objects.get(id=id)

	if request.method != "POST":

		formboi = CreationForm()
		formboi.inputs[0]["value"] = event.eventname
		formboi.inputs[1]["value"] = event.campusid.id
		formboi.inputs[2]["value"] = event.eventtypeid.id

		proposal_form = event.formproposalid
		logistic_form = event.formlogisticsid

		for proposal_question in proposal_form.getQuestions():
			formboi.inputs[3]["array"][event.eventtypeid.id]["questions"][proposal_question.id]["value"] = Answer.objects.filter(eventid_event=event, associatedformid=proposal_form, questionsid_questions=proposal_question)[0].answer
		for logistic_question in logistic_form.getQuestions():
			formboi.inputs[4]["array"][event.eventtypeid.id]["questions"][logistic_question.id]["value"] = Answer.objects.filter(eventid_event=event, associatedformid=logistic_form, questionsid_questions=logistic_question)[0].answer


		template = loader.get_template('create_new.html')
		context = {
			'form': formboi.inputs,
			'eventtypes': Eventtype.objects.all()
		}

		return HttpResponse(template.render(context, request))


	else:

		formboi = CreationForm(request)
		#form_name = request.POST['name']
		#form_campus = Campus.objects.get(id=request.POST['campus'])
		#form = Form.objects.get(id=request.POST['form_id'])



		proposal_form_type = Formtype.objects.get(typename="Proposal")
		logistic_form_type = Formtype.objects.get(typename="Logistic")

		name = formboi.inputs[0]["value"]
		campus = Campus.objects.get(id=int(formboi.inputs[1]["value"]))

		event_type = Eventtype.objects.get(id=int(formboi.inputs[2]["value"]))
		proposal_form = Form.objects.filter(formtypeid_formtype=proposal_form_type, eventtypeid=event_type, archived=False)[0]
		logistic_form = Form.objects.filter(formtypeid_formtype=logistic_form_type, eventtypeid=event_type, archived=False)[0]

		proposal_answers = formboi.inputs[3]["array"][event_type.id]["questions"].values()
		logistic_answers = formboi.inputs[4]["array"][event_type.id]["questions"].values()


		
		event.eventtypeid=event_type
		event.formresgistrationid=proposal_form	#dummy
		event.formfeedbackid=proposal_form	#dummy
		event.campusid=campus
		event.wasvalidated="0"
		event.proponentid=request.user
		event.eventname=name
		event.formproposalid=proposal_form
		event.formlogisticsid=logistic_form
		
		event.save()

		for answer in proposal_answers:
			if(answer["value"] == ''):
				continue

			Answer.objects.filter(eventid_event=event, associatedformid=proposal_form, questionsid_questions=answer["question_obj"]).delete()

			an = Answer(
				associatedformid=proposal_form,
				questionsid_questions=answer["question_obj"],
				eventid_event=event,
				answer=answer["value"],
				dateofcreation=datetime.datetime.now()
			)
			an.save()

		for answer in logistic_answers:

			if(answer["value"] == ''):
				continue

			Answer.objects.filter(eventid_event=event, associatedformid=logistic_form, questionsid_questions=answer["question_obj"]).delete()
			
			an = Answer(
				associatedformid=logistic_form,
				questionsid_questions=answer["question_obj"],
				eventid_event=event,
				answer=answer["value"],
				dateofcreation=datetime.datetime.now()
			)
			an.save()
			
		return redirect("list")