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
    if Resgistration.objects.filter(pk=RegistrationID).exists() :
        registration = Resgistration.objects.get(pk=RegistrationID)
    
    registration.cancelregistrations(request.user)
    registration.delete()
    return redirect("index")


def consultar_participantes(request,eventid_event) :
    if Event.objects.filter(pk=eventid_event).exists() :
        template = loader.get_template('participant.html')
        context = {
            'Registrations': Resgistration.objects.filter(eventid_event=eventid_event)
        }
        return HttpResponse(template.render(context, request))
    else:
        return redirect("index")
       
    
def addregistration(request, EventID= None):
    if not EventID or not Event.objects.filter(id=EventID) :
        errorMessage = "Error: No Event given"
    
    else :
        eventToRegister = Event.objects.get(id=EventID)
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

                template = loader.get_template('registersuc.html')
                context = {
                    'errorMessage' : errorMessage,
                }
                return HttpResponse(template.render(context, request))

        else:
            form = EventManagerForm(eventManagerFormID=eventToRegister.formresgistrationid.id, associatedRegistration=regis, associatedEvent=None)




    template = loader.get_template('template_test_form.html')
    context = {
        'form' : form,
    }
    return HttpResponse(template.render(context, request))


# def checkboxvalues(request)
    
#             template = loader.get_template('template_show_form_layout.html')
#     context = {
#         'form' : form,
#         'return_addr' : return_addr,
#         'errorMessage' : errorMessage,
#     }
#     return HttpResponse(template.render(context, request))