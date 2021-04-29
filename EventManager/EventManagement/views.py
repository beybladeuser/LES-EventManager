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
       
    



# def checkboxvalues(request)
    
#             template = loader.get_template('template_show_form_layout.html')
#     context = {
#         'form' : form,
#         'return_addr' : return_addr,
#         'errorMessage' : errorMessage,
#     }
#     return HttpResponse(template.render(context, request))