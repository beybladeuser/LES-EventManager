from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from PreEventManagement.models import *
from AssetManagement.models import *
from FormManagement.models import *

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

	proposal_form_type = Formtype.objects.get(typename="Proposal")
	proposal_forms = Form.objects.filter(formtypeid_formtype=proposal_form_type)
	event_proposal_form = proposal_forms.get(eventtypeid=event.eventtypeid)

	Answer.objects.filter(associatedformid=event_proposal_form, eventid_event=event).delete()
	event.delete()
	return redirect("list")


def create(request):
	event_types = Eventtype.objects.all()


	proposal_form_type = Formtype.objects.get(typename="Proposal")
	proposal_forms = Form.objects.filter(formtypeid_formtype=proposal_form_type)


	if request.method != "POST":
		template = loader.get_template('create.html')
		context = {
			'event_types': event_types,
			'default_event_type': event_types[0],

			'campuses': Campus.objects.all(),

			'forms': proposal_forms
		}

		return HttpResponse(template.render(context, request))
	else:
		form_name = request.POST['name']
		form_campus = Campus.objects.get(id=request.POST['campus'])
		form = Form.objects.get(id=request.POST['form_id'])


		ev = Event(
			eventtypeid=form.eventtypeid, 
			formresgistrationid=form,
			formfeedbackid=form,
			campusid=form_campus,
			wasvalidated="0",
			proponentid=request.user,
			eventname=form_name,
			formproposalid=form
		)
		ev.save()

		for key, val in request.POST.items():
			if key.startswith("val"):
				question = Questions.objects.get(id=key[3:])
				an = Answer(
					associatedformid=form,
					questionsid_questions=question,
					eventid_event=ev,
					answer=val,
					dateofcreation=datetime.datetime.now()
				)
				an.save()
		return redirect("list")











def list(request):
	proposal_form_type = Formtype.objects.get(typename="Proposal")
	events = Event.objects.all()
	for event in events:
		try:
			leform = Form.objects.get(formtypeid_formtype=proposal_form_type, eventtypeid=event.eventtypeid)
		except:
			raise Exception("An event (" + event.eventname + ") was created but there is no proposal form for it's type (or there are more than one).")

		form_questions = leform.getQuestions()
		if len(form_questions) == 0:
			raise Exception("Event type (" + event.eventtypeid.typename + ") proposal form with no questions")

		event.QAs = []
		for question in form_questions:
			answer2 = Answer.objects.filter(eventid_event=event, questionsid_questions=question, associatedformid=leform)
			print(answer2)
			try:
				answer = Answer.objects.get(eventid_event=event, questionsid_questions=question, associatedformid=leform)
			except:
				raise Exception("An event was created (" + event.eventname + ") but a question on it's proposal form (" + question.question + ") lacks an answer")

			event.QAs.append({
				"question": question,
				"answer": answer
			})
			if event.QAs[-1]["question"].questiontypeid_questiontype.typename == "Multiple Choice":
				event.QAs[-1]["answer"].answer = Multipleoptions.objects.get(id=event.QAs[-1]["answer"].answer).option
		#event.QAs = "henlo"


	template = loader.get_template('listEvent.html')
	context = {
		'eventes': events,
	}

	return HttpResponse(template.render(context, request))








def edit(request, id):
	event = Event.objects.get(id=id)
	proposal_form_type = Formtype.objects.get(typename="Proposal")
	
	
	try:
		leform = Form.objects.get(formtypeid_formtype=proposal_form_type, eventtypeid=event.eventtypeid)
	except:
		raise Exception("An event (" + event.eventname + ") was created but there is no proposal form for it's type (or there are more than one).")

	form_questions = leform.getQuestions()
	if len(form_questions) == 0:
		raise Exception("Event type (" + event.eventtypeid.typename + ") proposal form with no questions")

	event.QAs = []
	for question in form_questions:
		answer2 = Answer.objects.filter(eventid_event=event, questionsid_questions=question, associatedformid=leform)
		print(answer2)
		try:
			answer = Answer.objects.get(eventid_event=event, questionsid_questions=question, associatedformid=leform)
		except:
			raise Exception("An event was created (" + event.eventname + ") but a question on it's proposal form (" + question.question + ") lacks an answer")

		event.QAs.append({
			"question": question,
			"answer": answer
		})
		if event.QAs[-1]["question"].questiontypeid_questiontype.typename == "Multiple Choice":
			event.QAs[-1]["answer"].answer = Multipleoptions.objects.get(id=event.QAs[-1]["answer"].answer).option
			event.QAs[-1]["question"].possible_answers = Multipleoptions.objects.filter(questionsid_questions=question)


	template = loader.get_template('letsgo.html')
	context = {
		'eventes': events,
	}

	return HttpResponse(template.render(context, request))