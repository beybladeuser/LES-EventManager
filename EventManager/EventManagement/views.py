from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connection
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from FormManagement.forms import EventManagerForm
from Models.models import *

from .models import *

import datetime

# Create your views here.
def cancelregistration(request, RegistrationID = None) :
    registration=None
    if Resgistration.objects.filter(pk=RegistrationID).exists()  :
        registration = Resgistration.objects.get(pk=RegistrationID)
        
    if  registration and registration.canCancel() :
        registration.cancelregistrations(request.user)
        errorMessage = "Cancel registration successful"
        template = loader.get_template('message.html')
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
        template = loader.get_template('participant.html')
        context = {
            'registrations': Resgistration.objects.filter(eventid_event=eventid_event),
            'event' : event
        }
        return HttpResponse(template.render(context, request))
    else:
        errorMessage = "Event does not exist"
        template = loader.get_template('message.html')
        context = {
            'errorMessage' : errorMessage,
        }
        return HttpResponse(template.render(context, request))

def viewanswer(request, RegistrationID = None ):
        viewanswer = Answer.objects.all()
        template = loader.get_template('test.html')
        context = {
            'Answer': Answer.objects.filter(resgistrationid = RegistrationID),
            'viewanswer' : viewanswer
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


