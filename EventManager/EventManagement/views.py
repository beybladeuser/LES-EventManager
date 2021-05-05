from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import connection

from .models import *

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
       
    
def addregistration(request, formID = 1):
    regis = Resgistration()
    regis.eventid_event = Event.objects.get(id=1)
    regis.participantuserid = request.user
    if request.method == 'POST':
        form = EventManagerForm(request.POST, eventManagerFormID=formID, associatedRegistration=regis, associatedEvent=None)
        if form.is_valid():
            regis.save()
            answeredForm = form.save()
            request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(answeredForm.formtypeid_formtype.id)
            return redirect("checkFormLayout", answeredForm.id)
    
    else:
        form = EventManagerForm(eventManagerFormID=formID, associatedRegistration=regis, associatedEvent=None)
    
    


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