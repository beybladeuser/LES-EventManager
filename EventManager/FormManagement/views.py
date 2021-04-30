from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from Models.models import *

from .forms import *

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
                request.session['delete_form_return_redirect'] = "/forms/listformsfromtype/" + str(formTypeID)

        else :
            errorMessage = "Error: Invalid form type"
    else :
        errorMessage = "Error: No form type given"


    template = loader.get_template('template_list_forms.html')
    context = {
        'forms' : forms,
        'formType' : formType[0],
        'errorMessage' : errorMessage,
    }
    return HttpResponse(template.render(context, request))


def createForm(request, formTypeID=None, formID=None) :
    formCreate = None
    errorMessage = None
    formCreation_form = None
    if formTypeID and Formtype.objects.filter(id=formTypeID).exists() :
        if not formID or not Form.objects.filter(id=formID).exists() :
            formCreate = True
    else :
        errorMessage = "Error: No form type specified or invalid form type"
    
    if not errorMessage :
        if request.method == 'POST':
            formCreation_form = formCreation(request.POST)
            if formCreation_form.is_valid():
                newForm = formCreation_form.save(formID, request.user)
                request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(newForm.formtypeid_formtype.id)
                return redirect("checkFormLayout", newForm.id)

        else:
            if formCreate :
                formCreation_form = formCreation(initial={
                    'formType': formTypeID,
                })
            else :
                existing_form = Form.objects.get(pk=formID)
                formCreation_form = formCreation(initial={
                    'formId' : existing_form.id,
                    'formName': existing_form.formname,
                    'formType': existing_form.formtypeid_formtype.id,
                    'eventType': existing_form.eventtypeid.id
                })
    
    


    template = loader.get_template('template_create_new_form.html')
    context = {
        'formCreate' : formCreate,
        'errorMessage' : errorMessage,
        'formCreation' : formCreation_form
    }
    return HttpResponse(template.render(context, request))


def deleteForm_action(request, formID=None):
    return_addr="formsHome"
    return_addr = request.session.get('delete_form_return_redirect', return_addr)
    if return_addr != formsHome :
        del request.session['form_return_redirect']
        request.session.modified = True
    
    if formID and Form.objects.filter(id=formID).exists() :
        questionFormsRelations = QuestionsForm.objects.filter(formid_form=formID)
        for questionFormsRelation in questionFormsRelations:
            questionFormsRelation.delete()
        
        Form.objects.get(pk=formID).delete()

    return redirect(return_addr)


def testForm(request, formID = 1):
    if request.method == 'POST':
        form = EventManagerForm(request.POST, eventManagerFormID=formID, associatedRegistration=1, associatedEvent=None)
        if form.is_valid():
            answeredForm = form.save()
            request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(answeredForm.formtypeid_formtype.id)
            return redirect("checkFormLayout", answeredForm.id)
    
    else:
        form = EventManagerForm(eventManagerFormID=formID, associatedRegistration=1, associatedEvent=None)
    
    


    template = loader.get_template('template_test_form.html')
    context = {
        'form' : form,
    }
    return HttpResponse(template.render(context, request))