from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def preEventHome(request) :
    template = loader.get_template('preEventHome.html')
    context = {}
    return HttpResponse(template.render(context, request))
    
def eventList(request) :
    template = loader.get_template('eventList.html')
    context = {}
    return HttpResponse(template.render(context, request))