from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connection
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from .forms import EventManagerForm
from Models.models import *

from .models import *

import datetime

# Create your views here.

def index(request):
	template = loader.get_template('homePreEvent.html')
	context = {}
	return HttpResponse(template.render(context, request))


def cancelregistration(request, RegistrationID = None) :
    registration=None
    if Resgistration.objects.filter(pk=RegistrationID).exists()  :
        registration = Resgistration.objects.get(pk=RegistrationID)
        
    if  registration and registration.canCancel(request.user) :
        registration.cancelregistrations(request.user)
        errorMessage = "Cancel registration successful"
        template = loader.get_template('messageeliminar.html')
        context = {
        'errorMessage' : errorMessage,
        }
        return HttpResponse(template.render(context, request))  
    else:
        errorMessage = "Already checked in"
        template = loader.get_template('message.html')
        context = {
        'errorMessage' : errorMessage,
        }
    return HttpResponse(template.render(context, request))
    
        


def consultar_participantes(request,eventid_event) :
    if Event.objects.filter(pk=eventid_event).exists()  :
        event = Event.objects.get(pk=eventid_event)
        if event.canConsultParticipants(request.user) :
            template = loader.get_template('participant.html')
            context = {
                'registrations': Resgistration.objects.filter(eventid_event=eventid_event).order_by('participantuserid'),
                'event' : event
            }
            return HttpResponse(template.render(context, request))
        else:
            errorMessage = "can not access this page"
                
    else:
        errorMessage = "Event does not exist"

    template = loader.get_template('message.html')
    context = {
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def consultar_inscricoes(request) :
    registerEvents=None
    errorMessage=None
    if (not Resgistration.objects.filter(participantuserid=request.user.id).exists()) :
        errorMessage="Não está inscrito em nenhum evento"
        
    registerEvents=Resgistration.objects.filter(participantuserid=request.user.id)
    template = loader.get_template('myevents.html')
    context = {
        'registerEvents': registerEvents,
        'errorMessage' : errorMessage
    }
    return HttpResponse(template.render(context, request))

    


    
def addregistration(request, EventID= None):
    errorMessage = None
    form = None
    if not EventID or not Event.objects.filter(id=EventID).exists() :
        errorMessage = "Error: No Event given"
    
    else :
        eventToRegister = Event.objects.get(id=EventID)
        if not Resgistration.canRegister(eventToRegister, request.user) :
            errorMessage= "Already subscribed in this event"
        else :
            regis = Resgistration()
            regis.eventid_event = eventToRegister
            regis.participantuserid = request.user
            regis.waspresent = False
            regis.dateofregistration = datetime.datetime.now()
            if request.method == 'POST':
                form = EventManagerForm(request.POST, eventManagerFormID=eventToRegister.formresgistrationid.id, associatedRegistration=regis, associatedEvent=None)
                if form.is_valid():
                    regis.save()
                    answeredForm = form.save()

                    errorMessage = "Registration Successfull"

                    template = loader.get_template('message.html')
                    context = {
                        'errorMessage' : errorMessage,
                    }
                    return HttpResponse(template.render(context, request))

            else:
                form = EventManagerForm(eventManagerFormID=eventToRegister.formresgistrationid.id, associatedRegistration=regis, associatedEvent=None)
    template = loader.get_template('template_registration_form.html')
    context = {
        'form' : form,
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def viewanswer(request, RegistrationID = None ):
    answers = Answer.objects.filter(resgistrationid = RegistrationID)
    registration = None
    errorMessage = None
    if (Resgistration.objects.filter(pk=RegistrationID).exists()) :
        registration = Resgistration.objects.get(pk=RegistrationID)
        regisForm = registration.eventid_event.formresgistrationid
        regisQuestions = regisForm.getQuestions()
        answers = []
        for regisQuestion in regisQuestions :
            if (regisQuestion.getAnswersForForm(regisForm).filter(resgistrationid=RegistrationID).exists()) :
                answer = regisQuestion.getAnswersForForm(regisForm).get(resgistrationid=RegistrationID)
                answers.append( {"questionsid_questions":regisQuestion, "answer":answer.answer} )
            else :
                answers.append( {"questionsid_questions":regisQuestion, "answer":"N\\a"} )
    else :
        errorMessage = "Erro: Registo nao existe"
    template = loader.get_template('list_event_regs_form_answers.html')
    context = {
        'registration' : registration,
        'answers': answers,
        'errorMessage':errorMessage,
    }
    return HttpResponse(template.render(context, request))


def checkout(request, RegistrationID=None):
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changeCheckoutStatus(False)
    return redirect('consultar_participantes', regist.eventid_event.id)

def checkin(request,RegistrationID=None) :
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changeCheckoutStatus(True)
    return redirect('consultar_participantes', regist.eventid_event.id)


    
       
def validateparticipant(request,RegistrationID=None):
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changevalidateStatus(2)
    return redirect('consultar_participantesnaovalidados', regist.eventid_event.id)

def invalidateparticipant(request,RegistrationID=None):
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changevalidateStatus(1)
    return redirect('consultar_participantesnaovalidados', regist.eventid_event.id)

    

def pendenteparticipant(request,RegistrationID=None):
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changevalidateStatus(0)
    return redirect('consultar_participantesnaovalidados', regist.eventid_event.id)


def consultar_participantesnaovalidados(request,eventid_event) :
    if Event.objects.filter(pk=eventid_event).exists()  :
        event = Event.objects.get(pk=eventid_event)
        if event.canConsultParticipants(request.user) :
            template = loader.get_template('nonvalidateparticipantes.html')
            context = {
                'registrations': Resgistration.objects.filter(eventid_event=eventid_event).order_by('state'),
                'event' : event
            }
            return HttpResponse(template.render(context, request))
        else:
            errorMessage = "can not access this page"
                
    else:
        errorMessage = "Event does not exist"

    template = loader.get_template('message.html')
    context = {
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))