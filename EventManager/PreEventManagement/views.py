from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from PreEventManagement.models import *
from AssetManagement.models import *
from FormManagement.models import *
from EventManagement.models import *


def index(request):
	return redirect('list') 




def validate(request, id, validate):
	#0 event proposed
	#1 event proposal validated
	#2 event logistics validated (event ready)
	#-1 event proposal refused
	#-2 event logistics refused

	event = Event.objects.get(id=id)
	if validate == 1:
		event.wasvalidated+=1
	else:
		if event.wasvalidated == 0:
			event.wasvalidated = -1
		elif event.wasvalidated == 1:
			event.wasvalidated = -2
	event.save()

	return redirect("list")


def delete(request, id):
	event = Event.objects.get(id=id)

	Answer.objects.filter(associatedformid=event.formproposalid, eventid_event=event).delete()
	AssetEvent.objects.filter(eventid_event=event).delete()
	event.delete()
	return redirect("list")

#https://discord.com/channels/@me/541054920384839691/856168028520972308








#//////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////MAIN LIST//////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////



def listing(request, sort_key="00"): 
	proposal_form_type = Formtype.objects.get(id=1)
	sortnames = ['eventname', 'eventtypeid', "campusid", "wasvalidated", "proponentid__username"]
	events = Event.objects.order_by(('-' if int(sort_key[1:2])==1 else '')+sortnames[int(sort_key[0:1])])
	for event in events:
		try:
			proposal_form = event.formproposalid
	
		except:
			raise Exception("An event (" + event.eventname + ") was created but there is no proposal form for it's type (or there are more than one).")

		proposal_form_questions = proposal_form.getQuestions()
		#logistic_form_questions = logistic_form.getQuestions()
		if len(proposal_form_questions) == 0:
			raise Exception("Event type (" + event.eventtypeid.typename + ") proposal form with no questions")
		#if len(logistic_form_questions) == 0:
		#	raise Exception("Event type (" + event.eventtypeid.typename + ") logistics form with no questions")

		try:
			registration = Resgistration.objects.get(eventid_event=event, participantuserid=request.user)
		except Resgistration.DoesNotExist:
			registration = None
		event.user_was_present = False if registration is None else registration.waspresent
		event.currently_enrolled = -1 if registration is None else registration.state
		event.has_participants = Resgistration.objects.filter(eventid_event=event).exists()
		event.user_feedback_already = Answer.objects.filter(associatedformid=event.formfeedbackid, eventid_event=event, resgistrationid__participantuserid=request.user).exists()
		event.has_associated_assets = AssetEvent.objects.filter(eventid_event=event).exists()
		
		assetids = [x.assetid_asset for x in AssetEvent.objects.filter(eventid_event=event)]
		event.assets_equipment = Equipment.objects.filter(assetid__in=assetids).order_by("equipmenttypeid_equipmenttype")
		event.assets_service = Service.objects.filter(assetid__in=assetids).order_by("servicetypeid_servicetype")
		event.assets_room = Rooms.objects.filter(assetid__in=assetids).order_by("room_type")
		event.has_equipment_assets = event.assets_equipment.exists()
		event.has_service_assets = event.assets_service.exists()
		event.has_room_assets = event.assets_room.exists()


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

		#event.logistic_QAs = []
		#for question in logistic_form_questions:
		#	try:
		#		answer = Answer.objects.get(eventid_event=event, questionsid_questions=question, associatedformid=logistic_form)
		#	except:
		#		if question.required:
		#			raise Exception("An event was created (" + event.eventname + ") but a question on it's logistics form (" + question.question + ") lacks an answer")
		#		else:
		#			print("NOT NEEDED")
		#			continue
		#			
		#	QA = {
		#		"question": question,
		#		"answer": answer
		#	}
		#	QA["answer"].has_text = False
		#	if(QA["question"].questiontypeid_questiontype.id == 2):
		#		QA["answer"].has_text = True
		#		QA["answer"].text = Multipleoptions.objects.get(id=int(answer.answer)).option
		#	elif(QA["question"].questiontypeid_questiontype.id > 2):
		#		QA["answer"].has_text = True
		#		QA["answer"].text = Form.objects.get(id=int(answer.answer)).formname
		#		
		#	event.logistic_QAs.append(QA)


	template = loader.get_template('listEvent_new.html')
	context = {
		'filterKey': sort_key,
		'eventTypes': Eventtype.objects.all(),
		'campuses': Campus.objects.all(),
		'eventes': events,
		'user': request.user
	}

	return HttpResponse(template.render(context, request))






















#//////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////PROPOSALS//////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////


def ziplist(list1, list2): return [[i, j] for i, j in zip(list1,list2)]

def build_form(generic_name, form):

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
		questions[currquestion.id] = question

	return questions



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
		]

	def __init__(self, user, request=None):
		self.__initvars()

		proposal_form_type = Formtype.objects.get(id=1)
		proposal_forms = (
			Form.objects.filter(formtypeid_formtype=proposal_form_type, archived=False, published=False, createdby=user)
			|
			Form.objects.filter(formtypeid_formtype=proposal_form_type, archived=False, published=True)
		)
		#logistics_form_type = Formtype.objects.get(id=4)
		#logistics_forms = Form.objects.filter(formtypeid_formtype=logistics_form_type, archived=False)


		for form in proposal_forms: 
			if form.getQuestions().exists():
				self.inputs[3]['array'][form.eventtypeid.id] = {
					'name': 'proposalform_'+str(form.eventtypeid.id),

					'eventtype': form.eventtypeid.id,
					'formid': form.id,

					'formobj': form,

					'questions': build_form("proposalform", form)
				}
		#for form in logistics_forms: 
		#	if form.getQuestions().count() > 0:
		#		self.inputs[4]['array'][form.eventtypeid.id] = {
		#			'name': 'logisticsform_'+str(form.eventtypeid.id),
		#			
		#			'eventtype': form.eventtypeid.id,
		#			'formid': form.id,
		#			
		#			'questions': self.__build_form("logisticsform", form)
		#		}

		if request != None:
			self.inputs[0]["value"] = request.POST.get(self.inputs[0]["name"])
			self.inputs[1]["value"] = request.POST.get(self.inputs[1]["name"])
			self.inputs[2]["value"] = request.POST.get(self.inputs[2]["name"])
			for eachform in self.inputs[3]["array"].values():
				for eachquestion in eachform['questions'].values():
					eachquestion["value"] = request.POST.get(eachquestion["name"])
			#for eachform in self.inputs[4]["array"].values():
			#	for eachquestion in eachform["questions"].values():
			#		eachquestion["value"] = request.POST.get(eachquestion["name"])






def create(request):




	if request.method != "POST":
		formboi = CreationForm(request.user)
		template = loader.get_template('create_new.html')

		context = {
			'form': formboi.inputs,
			'eventtypes': Eventtype.objects.all(),
			'enabled_by_default': 
					(formboi.inputs[2]["choices"][0][0] in formboi.inputs[3]["array"]) #and formboi.inputs[2]["choices"][0][0] in formboi.inputs[4]["array"])  
				if (formboi.inputs[2]["value"] == None) else  
					(int(formboi.inputs[2]["value"]) in formboi.inputs[3]["array"])# and int(formboi.inputs[2]["value"]) in formboi.inputs[4]["array"])
		}

		print("WHYYYYYYY: " + str(formboi.inputs[2]["value"]))
		return HttpResponse(template.render(context, request))
	else:
		formboi = CreationForm(request.user, request)
	


		proposal_form_type = Formtype.objects.get(id=1)
	


		name = formboi.inputs[0]["value"]
		campus = Campus.objects.get(id=int(formboi.inputs[1]["value"]))

		event_type = Eventtype.objects.get(id=int(formboi.inputs[2]["value"]))
		
		proposal_form = formboi.inputs[3]['array'][event_type.id]['formobj']
	

		proposal_answers = formboi.inputs[3]["array"][event_type.id]["questions"].values()



		ev = Event(
			eventtypeid=event_type, 
			formresgistrationid=None,
			formfeedbackid=None,
			campusid=campus,
			wasvalidated=0,
			proponentid=request.user,
			eventname=name,
			formproposalid=proposal_form,
		
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

		#for answer in logistic_answers:
		#	
		#	if(answer["value"] == ''):
		#		continue
		#		
		#	an = Answer(
		#		associatedformid=logistic_form,
		#		questionsid_questions=answer["question_obj"],
		#		eventid_event=ev,
		#		answer=answer["value"],
		#		dateofcreation=datetime.datetime.now()
		#	)
		#	an.save()
			
		return redirect("list")



def edit(request, id):

	event = Event.objects.get(id=id)

	if request.method != "POST":

		formboi = CreationForm(request.user)
		formboi.inputs[0]["value"] = event.eventname
		formboi.inputs[1]["value"] = event.campusid.id
		formboi.inputs[2]["value"] = event.eventtypeid.id

		proposal_form = event.formproposalid
		

		for proposal_question in proposal_form.getQuestions():
			answer_queryset = Answer.objects.filter(eventid_event=event, associatedformid=proposal_form, questionsid_questions=proposal_question)
			formboi.inputs[3]["array"][event.eventtypeid.id]["questions"][proposal_question.id]["value"] = "" if not answer_queryset.exists() else answer_queryset[0].answer
		#for logistic_question in logistic_form.getQuestions():
		#	answer_queryset = Answer.objects.filter(eventid_event=event, associatedformid=logistic_form, questionsid_questions=logistic_question)
		#	formboi.inputs[4]["array"][event.eventtypeid.id]["questions"][logistic_question.id]["value"] = "" if answer_queryset.count()==0 else answer_queryset[0].answer


		template = loader.get_template('create_new.html')
		context = {
			'form': formboi.inputs,
			'eventtypes': Eventtype.objects.all(),
			'enabled_by_default': True
		}

		return HttpResponse(template.render(context, request))


	else:

		formboi = CreationForm(request.user, request)
		#form_name = request.POST['name']
		#form_campus = Campus.objects.get(id=request.POST['campus'])
		#form = Form.objects.get(id=request.POST['form_id'])



		proposal_form_type = Formtype.objects.get(id=1)
		#logistic_form_type = Formtype.objects.get(typename="Logistic")

		name = formboi.inputs[0]["value"]
		campus = Campus.objects.get(id=int(formboi.inputs[1]["value"]))

		event_type = Eventtype.objects.get(id=int(formboi.inputs[2]["value"]))
		
		proposal_form = formboi.inputs[3]['array'][event_type.id]['formobj']
		#proposal_form = Form.objects.filter(formtypeid_formtype=proposal_form_type, eventtypeid=event_type, archived=False)[0]
		#logistic_form = Form.objects.filter(formtypeid_formtype=logistic_form_type, eventtypeid=event_type, archived=False)[0]

		proposal_answers = formboi.inputs[3]["array"][event_type.id]["questions"].values()
		#logistic_answers = formboi.inputs[4]["array"][event_type.id]["questions"].values()


		
		event.eventtypeid=event_type 
		event.formresgistrationid=None
		event.formfeedbackid=None
		event.campusid=campus
		event.wasvalidated=0
		event.proponentid=request.user
		event.eventname=name
		event.formproposalid=proposal_form
	
		
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
			
		return redirect("list")





















#//////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////LOGISTICS//////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////



class LogisticForm:


	def __init__(self, user, event, request=None):
		eventtype = event.eventtypeid

		registration_form_type = Formtype.objects.get(id=2)
		feedback_form_type = Formtype.objects.get(id=3)

		registration_forms = (
			Form.objects.filter(formtypeid_formtype=registration_form_type, eventtypeid=eventtype, archived=False, published=False, createdby=user)
			|
			Form.objects.filter(formtypeid_formtype=registration_form_type, eventtypeid=eventtype, archived=False, published=True)
		)

		feedback_forms = (
			Form.objects.filter(formtypeid_formtype=feedback_form_type, eventtypeid=eventtype, archived=False, published=False, createdby=user)
			|
			Form.objects.filter(formtypeid_formtype=feedback_form_type, eventtypeid=eventtype, archived=False, published=True)
		)

		self.inputs = [
			{
				'type': 'hrline',
				'identifier': 'Formulários',
				'topbreak': False
			},
			{
				'name': 'registration_form',
				'identifier': 'Registration form',
				'type': 'dropdown',
				'optional': False,
				'nochoice': "Formulário de registo indisponível para \""+event.eventtypeid.typename+"\", crie ou desarquive um formulário de registo para prosseguir.",
				'choices': ziplist(
					[x.id for x in registration_forms],
					[x.formname for x in registration_forms]
				),
				'value': None
			},
			{
				'name': 'feedback_form',
				'identifier': 'Feedback form',
				'type': 'dropdown',
				'optional': True,
				'nochoice': "Formulário de feedback indisponível para \""+event.eventtypeid.typename+"\", crie ou desarquive um formulário de registo para prosseguir.",
				'choices': ziplist(
					[x.id for x in feedback_forms],
					[x.formname for x in feedback_forms]
				),
				'value': None
			},
		]

		if request != None:
			self.inputs[1]["value"] = request.POST.get(self.inputs[1]["name"])
			self.inputs[2]["value"] = request.POST.get(self.inputs[2]["name"])


		#------------------------------------------------------------------------------------------- equipment
		self.inputs.append({
			'type': 'hrline',
			'identifier': 'Equipamento',
			'topbreak': True
		})

		for equipment_type in Equipmenttype.objects.all():
			equipment_list = Equipment.objects.filter(equipmenttypeid_equipmenttype=equipment_type)
			asset_events = AssetEvent.objects.filter(
				eventid_event=event, 
				assetid_asset__in=[x.assetid for x in equipment_list]
			)

			curr_input = {
				'name': 'equipment_list'+str(equipment_type.id),
				'object': equipment_type,
				'identifier': equipment_type.typename,
				'type': 'multidropdown',
				'nochoice': "Não existem equipamentos nesta categoria.",
				'choices': ziplist(
					[x.assetid.id for x in equipment_list],
					[x.assetid.assetname for x in equipment_list]
				),
				'value': None if not asset_events.exists() else [x.assetid_asset for x in asset_events]
			}
			if(request != None):
				curr_input["value"] = []
				#print("--------------------------------")
				#print('equipment_list'+str(equipment_type.id)+'_count')
				count_var = request.POST.get('equipment_list'+str(equipment_type.id)+'_count')
				if count_var is not None:
					count = int(count_var)
					for i in range(count):
						asset_id = int(request.POST.get('equipment_list'+str(equipment_type.id)+'_'+str(i)))
						curr_input['value'].append(Asset.objects.get(id=asset_id))

			self.inputs.append(curr_input)



		#------------------------------------------------------------------------------------------- services
		self.inputs.append({
			'type': 'hrline',
			'identifier': 'Serviços',
			'topbreak': True
		})
		
		for service_type in Servicetype.objects.all():
			service_list = Service.objects.filter(servicetypeid_servicetype=service_type)
			asset_events = AssetEvent.objects.filter(
				eventid_event=event, 
				assetid_asset__in=[x.assetid for x in service_list]
			)
			curr_input = {
				'name': 'service_list'+str(service_type.id),
				'object': service_type,
				'identifier': service_type.typename,
				'type': 'multidropdown',
				'nochoice': "Não existem serviços nesta categoria.",
				'choices': ziplist(
					[x.assetid.id for x in service_list],
					[x.assetid.assetname for x in service_list]
				),
				'value': None if not asset_events.exists() else [x.assetid_asset for x in asset_events]
			}
			if(request != None):
				curr_input["value"] = []
				count_var = request.POST.get('service_list'+str(service_type.id)+'_count')
				if count_var is not None:
					count = int(count_var)
					for i in range(count):
						asset_id = int(request.POST.get('service_list'+str(service_type.id)+'_'+str(i)))
						curr_input['value'].append(Asset.objects.get(id=asset_id))

			self.inputs.append(curr_input)


		#------------------------------------------------------------------------------------------- rooms
		self.inputs.append({#2
			'type': 'hrline',
			'identifier': 'Salas',
			'topbreak': True
		})
		for room_type in RoomType.objects.all():
			room_list = Rooms.objects.filter(room_type=room_type)
			asset_events = AssetEvent.objects.filter(
				eventid_event=event, 
				assetid_asset__in=[x.assetid for x in room_list]
			)
			curr_input = {
				'name': 'room_list'+str(room_type.id),
				'object': room_type,
				'identifier': room_type.typename,
				'type': 'multidropdown',
				'nochoice': "Não existem salas nesta categoria.",
				'choices': ziplist(
					[x.assetid.id for x in room_list],
					[x.assetid.assetname for x in room_list]
				),
				'value': None if not asset_events.exists() else [x.assetid_asset for x in asset_events]
			}
			if(request != None):
				curr_input["value"] = []
				count_var = request.POST.get('room_list'+str(room_type.id)+'_count')
				if count_var is not None:
					count = int(count_var)
					for i in range(count):
						asset_id = int(request.POST.get('room_list'+str(room_type.id)+'_'+str(i)))
						curr_input['value'].append(Asset.objects.get(id=asset_id))

			self.inputs.append(curr_input)
		#------------------------------------------------------------------------------------------- /


def fill_logistic(request, id):
	event = Event.objects.get(id=id)

	if request.method != "POST":

		formboi = LogisticForm(request.user, event)

		template = loader.get_template('logistics.html')
		context = {
			'inputs': formboi.inputs,
			'form': formboi.inputs,
			'event': event
		}

		return HttpResponse(template.render(context, request))
	else:
		formboi = LogisticForm(request.user, event, request)

		event.formresgistrationid = Form.objects.get(id=int(formboi.inputs[1]["value"]))
		if not (not formboi.inputs[2]["value"] or formboi.inputs[2]["value"] is None):
			event.formfeedbackid = Form.objects.get(id=int(formboi.inputs[1]["value"]))
		event.save()

		AssetEvent.objects.filter(eventid_event=event).delete()
		for p in formboi.inputs:
			if 'value' not in p: continue
			if not isinstance(p["value"], list): continue
			for asset in p["value"]:
				assetevent = AssetEvent()
				assetevent.eventid_event = event
				assetevent.assetid_asset = asset
				assetevent.save()
	return redirect("list")


def edit_logistic(request, id):
	event = Event.objects.get(id=id)

	if request.method != "POST":

		formboi = LogisticForm(request.user, event)
		formboi.inputs[1]["value"] = event.formresgistrationid.id
		formboi.inputs[2]["value"] = event.formfeedbackid.id if event.formfeedbackid is not None else None

		template = loader.get_template('logistics.html')
		context = {
			'inputs': formboi.inputs,
			'form': formboi.inputs,
			'event': event
		}

		return HttpResponse(template.render(context, request))
	else:
		formboi = LogisticForm(request.user, event, request)

		event.formresgistrationid = Form.objects.get(id=int(formboi.inputs[1]["value"]))
		if not (not formboi.inputs[2]["value"] or formboi.inputs[2]["value"] is None):
			event.formfeedbackid = Form.objects.get(id=int(formboi.inputs[2]["value"]))
		else:
			event.formfeedbackid = None
		if event.wasvalidated == -2:
			event.wasvalidated = 1
		event.save()

		AssetEvent.objects.filter(eventid_event=event).delete()
		for p in formboi.inputs:
			if 'value' not in p: continue
			if not isinstance(p["value"], list): continue
			for asset in p["value"]:
				assetevent = AssetEvent()
				assetevent.eventid_event = event
				assetevent.assetid_asset = asset
				assetevent.save()
	return redirect("list")


def remove_all_assets(request, id):
	event = Event.objects.get(id=id)
	AssetEvent.objects.filter(eventid_event=event).delete()
	return redirect("list")









#//////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////FEEDBACK//////////////////////////////////////
#//////////////////////////////////////////////////////////////////////////////////////

class DynForm:

	def __init__(self, form, request=None):


		self.inputs = [
			{#0
				'name': 'dynform',
				'type': 'eachform',
				'questions': build_form('dynform', form)
			},
		]


		if request != None:
			for eachquestion in self.inputs[0]['questions'].values():
				eachquestion["value"] = request.POST.get(eachquestion["name"])


def feedback(request, id):
	event = Event.objects.get(id=id)
	feedback_form = event.formfeedbackid

	if request.method != "POST":

		formboi = DynForm(feedback_form)


		template = loader.get_template('dynform.html')
		context = {
			'title': 'Register in <i>' + event.eventname + '</i>',
			'form': formboi.inputs[0]
		}
		return HttpResponse(template.render(context, request))
	
	else:
		formboi = DynForm(feedback_form, request)
		for question in formboi.inputs[0]["questions"].values():
			#print('????????????????????????????????????????')
			#print(question)
			if question["value"] and not question["value"].isspace():
				an = Answer(
					associatedformid=feedback_form,
					questionsid_questions=question["question_obj"],
					eventid_event=event,
					answer=question["value"],
					dateofcreation=datetime.datetime.now(),
					resgistrationid=Resgistration.objects.get(eventid_event=event, participantuserid=request.user)
				)
				an.save()

		#reg = Resgistration(
		#	eventid_event=event,
		#	dateofregistration=datetime.datetime.now(),
		#	waspresent=False,
		#	participantuserid=request.user
		#)
		#reg.save()
	return redirect("list")


