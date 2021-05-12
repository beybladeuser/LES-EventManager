from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse


def homepage(request) :

    template = loader.get_template('template_base.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))

def narbar(request) :

    template = loader.get_template('navbar.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))


def welcome_screen(request) :

    template = loader.get_template('welcome_screen.html')
    context = {
        'isLoggedIn' : request.user.is_authenticated
    }
    return HttpResponse(template.render(context, request))

    