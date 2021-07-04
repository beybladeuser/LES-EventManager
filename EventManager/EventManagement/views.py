from django.db.models.query_utils import RegisterLookupMixin
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connection
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from .forms import EventManagerForm
#from Models.models import *

from .models import *

import datetime

# Create your views here.


def index(request):
	template = loader.get_template('homePreEvent.html')
	context = {}
	return HttpResponse(template.render(context, request))



        

#............................................funcoes de listagem............................................................
def consultar_participantes(request,eventid_event, key = None) :
    if Event.objects.filter(pk=eventid_event).exists()  :
        event = Event.objects.get(pk=eventid_event)
        if event.canConsultParticipants(request.user) :
            setToOrder = Resgistration.objects.filter(eventid_event=eventid_event)
            orderedSet = Resgistration.sortByKey(setToOrder, key)
            template = loader.get_template('participant.html')
            context = {
                'registrations': orderedSet,
                'event' : event,
                'filterKey' : key,
            }
            return HttpResponse(template.render(context, request))
        else:
            errorMessage = "Sem permissão para aceder a esta página"
                
    else:
        errorMessage = "O evento não existe"

    template = loader.get_template('message.html')
    context = {
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def consultar_participantesnaovalidados(request,eventid_event,key=None) :
    if Event.objects.filter(pk=eventid_event).exists()  :
        event = Event.objects.get(pk=eventid_event)
        setToOrder = Resgistration.objects.filter(eventid_event=eventid_event)
        orderedSet = Resgistration.sortByKey(setToOrder, key)
        if event.canConsultParticipants(request.user) :
            template = loader.get_template('nonvalidateparticipantes.html')
            context = {
                'registrations': orderedSet,
                'event' : event,
                'filterKey' : key
            }
            return HttpResponse(template.render(context, request))
        else:
            errorMessage = "Sem permissão para aceder a esta página"
                
    else:
        errorMessage = "O evento não existe"

    template = loader.get_template('message.html')
    context = {
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def consultar_inscricoes(request,key = None) :
    registerEvents=None
    errorMessage=None
    setToOrder = Resgistration.objects.filter(participantuserid=request.user.id)
    orderedSet = Resgistration.sortByKey(setToOrder, key)
    if (not Resgistration.objects.filter(participantuserid=request.user.id).exists()) :
        errorMessage="Não está inscrito em nenhum evento"
        
    
    template = loader.get_template('myevents.html')
    context = {
        'registerEvents': orderedSet,
        'errorMessage' : errorMessage,
        'filterKey' : key
    }
    return HttpResponse(template.render(context, request))

    
#............................................OVER funcoes de listagem............................................

#............................................funcoes de cancelar e add regis............................................    
def addregistration(request, EventID= None):
    errorMessage = None
    form = None
    if not EventID or not Event.objects.filter(id=EventID).exists() :
        errorMessage = "Error: Sem evento"
    
    else :
        eventToRegister = Event.objects.get(id=EventID)
        if not Resgistration.canRegister(eventToRegister, request.user) :
            errorMessage= "Já está marcado com presente neste evento"
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

                    errorMessage = "Inscrição feita com sucesso"

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

def cancelregistration(request, RegistrationID = None) :
    registration=None
    if Resgistration.objects.filter(pk=RegistrationID).exists()  :
        registration = Resgistration.objects.get(pk=RegistrationID)
        
    if  registration and registration.canCancel(request.user) :
        registration.cancelregistrations(request.user)
        errorMessage = "A sua inscrição foi cancelada"
        template = loader.get_template('messageeliminar.html')
        context = {
        'errorMessage' : errorMessage,
        }
        return HttpResponse(template.render(context, request))  
    else:
        errorMessage = "Já está marcado como presente no evento"
        template = loader.get_template('message.html')
        context = {
        'errorMessage' : errorMessage,
        }
    return HttpResponse(template.render(context, request))
#............................................OVER funcoes de cancelar e add regis............................................
#............................................funcao de ver resposta............................................
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
#............................................OVER funcao de ver resposta............................................


#............................................funcoes de alteracao de estado e presença............................................
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

    
#nao esta a ser usado mas podera vir a ser preciso futuramente
def pendenteparticipant(request,RegistrationID=None):
    if (RegistrationID and Resgistration.objects.filter(pk=RegistrationID).exists()):
        regist = Resgistration.objects.get(pk=RegistrationID)
        if regist.canCancelCheckout(request.user):
            regist.changevalidateStatus(0)
    return redirect('consultar_participantesnaovalidados', regist.eventid_event.id)

#............................................OVER funcoes de alteracao de estado e presença............................................
