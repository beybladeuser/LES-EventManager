from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import *

# Create your views here.
def cancelregistration(request, RegistrationID = None) :
    if Resgistration.objects.filter(pk=RegistrationID).exists() :
        registration = Resgistration.objects.get(pk=RegistrationID)
    
    registration.cancelregistrations(request.user)
    registration.delete()
    return redirect("index")