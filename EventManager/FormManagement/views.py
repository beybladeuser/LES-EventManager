from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from Models.models import *

def formsHome(request) :

    formTypes = Formtype.objects.all()
    errorMessage = None
    if not formTypes :
        errorMessage = "Error: No form types found on data base"
    
    template = loader.get_template('template_forms_home.html')
    context = {
        'formTypes' : formTypes,
        'errorMessage' : errorMessage,
        'isLogged' : request.user.is_authenticated,
    }
    return HttpResponse(template.render(context, request))

def checkFormLayout(request, formID = None, return_addr = '/forms/listformsfromtype/') :
    errorMessage = None
    form = None
    if formID :
        form_query = Form.objects.filter(id=formID)
        if not form_query :
            errorMessage = "Error: Form doesn't exist"
        else :
            form = form_query[0]
    
    else :
        errorMessage = "Error: No Form ID given"

    return_addr = request.session.get('form_return_redirect', return_addr)
    #if return_addr != '/forms/listformsfromtype/' :
    #    del request.session['form_return_redirect']
    #    request.session.modified = True

    
    template = loader.get_template('template_show_form_layout.html')
    context = {
        'form' : form,
        'return_addr' : return_addr,
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))

# Create your views here.
def checkForm(request, formID = None, return_addr = '/forms/listformsfromtype/') :
    #add the rerouting to login screen if user is not logged in
    formType = None
    eventType = None
    questions = None
    errorMessage = None
    if formID :
        Form_to_check = Form.objects.filter(pk=formID)
        if Form_to_check :
            formType = Form_to_check[0].getFormType()
            evetType = Form_to_check[0].getEventType()
            questions = Form_to_check[0].getQuestions()
        else :
            errorMessage = 'Invalid Form ID: Form doesn\'t exist'
    else:
        errorMessage = 'Invalid Form ID: No ID given'

    return_addr = request.session.get('form_return_redirect', return_addr)
    if return_addr != '/forms/listformsfromtype/' :
        del request.session['form_return_redirect']
        request.session.modified = True
    

    template = loader.get_template('template_show_form.html')
    context = {
        'formType' : formType,
        'eventType' : eventType,
        'questions' : questions,
        'return_addr' : return_addr,
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))

def listFormsFromType(request, formTypeID = None) :
    errorMessage = None
    formType = None
    forms = None
    if formTypeID :
        formType = Formtype.objects.filter(id=formTypeID)
        if formType :
            forms = Form.objects.filter(formtypeid_formtype=formTypeID)
            if not forms :
                errorMessage = "Error: No forms of type " + formType[0].typename
            else :
                request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(formTypeID)

        else :
            errorMessage = "Error: Invalid form type"
    else :
        errorMessage = "Error: No form type given"


    template = loader.get_template('template_list_forms.html')
    context = {
        'forms' : forms,
        'formType' : formType,
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def createForm(request, formTypeID=None, formID=None) :
    formCreate = None
    errorMessage = None
    if formTypeID :
        if not formID :
            formCreate = True
    else :
        errorMessage = "Error: No form type specified"

    template = loader.get_template('template_create_new_form.html')
    context = {
        'formCreate' : formCreate,
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))