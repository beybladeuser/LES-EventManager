from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request) :

    template = loader.get_template('template_index.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))

def homepage(request) :

    template = loader.get_template('homepage.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))

