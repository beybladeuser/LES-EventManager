from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from FormManagement.models import Form, Formtype, QuestionsForm, Questions, Multipleoptions, Questiontype, Answer
from Models.models import *

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from .forms import *
from .tables import *
from .filters import *

from utilizadores.views import user_check

def formsHome(request) :

    formTypes = Formtype.objects.all()
    errorMessage = None
    if not formTypes :
        errorMessage = "Erro: Não foram encontrados tipos de fomulário na base de dados"

    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"
    request.session["createQuestion_cancelRedirect"] = reverse('formsHome')
    request.session["createForm_cancelRedirect"] = reverse('formsHome')
    template = loader.get_template('template_forms_home.html')
    context = {
        'formTypes' : formTypes,
        'errorMessage' : errorMessage,
        'isLogged' : request.user.is_authenticated,
    }
    return HttpResponse(template.render(context, request))

def checkFormLayout(request, formID = None, filterKey=None) :
    errorMessage = None
    form = None
    canEdit = False
    questions = None
    return_addr = '/forms/listformsfromtype/'
    if formID :
        form_query = Form.objects.filter(id=formID)
        if not form_query :
            errorMessage = "Erro: Formulário não existe"
        else :
            form = form_query[0]
            return_addr = return_addr + str(form.formtypeid_formtype.id)
    
    else :
        errorMessage = "Erro: Nenhum formulário dado"

    if form :
        form.canEdit = form.canEdit(request.user)
        form.canDuplicate = form.canDuplicate(request.user)
        request.session["deleteOption_form_redirect"] = formID
        request.session["createOption_form_redirect"] = formID
        if not form.canDisplay(request.user):
            errorMessage = "Erro: Utilizador não possui acesso a esta pagina"


    return_addr = request.session.get('form_return_redirect', return_addr)
    #if return_addr != '/forms/listformsfromtype/' :
    #    del request.session['form_return_redirect']
    #    request.session.modified = True
    
    
    if form :
        questions = form.formquestions
        questions = Questions.sortByKey(questions, filterKey)
        if questions :
            for question in questions :
                question.canEdit = question.canEdit(request.user)
                question.canDuplicate = question.canDuplicate(request.user)

    if formID != None :
        if filterKey :
            request.session["createQuestion_cancelRedirect"] = reverse('checkFormLayout', args =[formID, filterKey])
            request.session["createOption_cancelRedirect"] = reverse('checkFormLayout', args =[formID, filterKey])
        else :
            request.session["createQuestion_cancelRedirect"] = reverse('checkFormLayout', args =[formID])
            request.session["createOption_cancelRedirect"] = reverse('checkFormLayout', args =[formID])
    else :
        request.session["createQuestion_cancelRedirect"] = reverse('checkFormLayout')
        request.session["createOption_cancelRedirect"] = reverse('checkFormLayout')

    template = loader.get_template('template_show_form_layout.html')
    context = {
        'questionTypes' : Questiontype.objects.all(),
        'form' : form,
        'questions' : questions,
        'return_addr' : return_addr,
        'errorMessage' : errorMessage,
        'filterKey' : filterKey,
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

    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"

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

def listFormsFromType(request, formTypeID = None, filterKey = None) :
    errorMessage = None
    formType = None
    formTypes = None
    forms = None
    if formTypeID :
        formTypes = Formtype.objects.filter(id=formTypeID)
        if formTypes :
            formType = formTypes[0]
            forms = Form.objects.filter(formtypeid_formtype=formTypeID)
            if not forms :
                errorMessage = "Erro: Nenhum formulário do tipo " + formType.typename
            else :
                request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(formTypeID)
                request.session['delete_form_return_redirect'] = "/forms/listformsfromtype/" + str(formTypeID)

        else :
            errorMessage = "Erro: Tipo de formulário invalido"
    else :
        errorMessage = "Erro: Nenhum tipo de evento dado"

    if forms :
        forms = Form.sortByKey(forms, filterKey)
        for form in forms :
            form.canEdit = form.canEdit(request.user)
            form.canDuplicate = form.canDuplicate(request.user)

    filterOptions = Form.getFilterOptions()
    eventTypes = Eventtype.objects.all()
    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"

    if formTypeID != None :
        if filterKey :
            request.session["createForm_cancelRedirect"] = reverse('listFormsFromType', args =[formTypeID, filterKey])
        else :
            request.session["createForm_cancelRedirect"] = reverse('listFormsFromType', args =[formTypeID])
    else :
        request.session["createForm_cancelRedirect"] = reverse('listFormsFromType')
    
    template = loader.get_template('template_list_forms.html')
    context = {
        'filterOptions' : filterOptions,
        'eventTypes' : eventTypes,
        'forms' : forms,
        'formType' : formType,
        'errorMessage' : errorMessage,
        'filterKey' : filterKey,
    }
    return HttpResponse(template.render(context, request))


class listFormsFromType_new(SingleTableMixin, FilterView) :
    table_class = formsTable
    template_name = 'template_list_forms.html'
    filterset_class = formsFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        user_check_var = user_check(request=request, user_profile=[Administrador, Proponente])
        if not user_check_var.get('exists'):
            return user_check_var.get('render')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        table.request = self.request
        table.fixed = True
        context[self.get_context_table_name(table)] = table
        return context


def createForm(request, formTypeID=None, formID=None) :
    formCreate = None
    errorMessage = None
    formCreation_form = None

    if formID and Form.objects.filter(id=formID).exists():
        formToEdit = Form.objects.get(pk=formID)
        if not formToEdit.canEdit(request.user) :
            errorMessage = "Erro: Utilizador não pode editar este formulário"
    elif request.user.groups.filter(pk=2).exists():
        errorMessage = "Erro: Participante não pode criar formulários, a conta deve ser do tipo Proponente ou Administrator"

    if not errorMessage :
        if formTypeID and Formtype.objects.filter(id=formTypeID).exists() :
            if not formID or not Form.objects.filter(id=formID).exists() :
                formCreate = True
        else :
            errorMessage = "Erro: Não foi especificado o tipo de formulário ou este é invalido"
    
    if not errorMessage :
        if request.method == 'POST':
            formCreation_form = formCreation(request.POST, currentUser=request.user)
            if formCreation_form.is_valid():
                newForm = formCreation_form.save(formID)
                request.session['form_return_redirect'] = "/forms/listformsfromtype/" + str(newForm.formtypeid_formtype.id)
                return redirect("checkFormLayout", newForm.id)

        else:
            if formCreate :
                formCreation_form = formCreation(currentUser=request.user,initial={
                    'formType': formTypeID,
                })
            else :
                existing_form = Form.objects.get(pk=formID)
                formCreation_form = formCreation(currentUser=request.user,initial={
                    'formId' : existing_form.id,
                    'formName': existing_form.formname,
                    'formType': existing_form.formtypeid_formtype.id,
                    'eventType': existing_form.eventtypeid.id
                })
    
    
    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"

    cancelRedirect = request.session.get("createForm_cancelRedirect", None)
    template = loader.get_template('template_create_new_form.html')
    context = {
        'formCreate' : formCreate,
        'errorMessage' : errorMessage,
        'formCreation' : formCreation_form,
        'cancelRedirect' : cancelRedirect
    }
    return HttpResponse(template.render(context, request))


def deleteForm_action(request, formID=None):
    return_addr="formsHome"
    return_addr = request.session.get('delete_form_return_redirect', return_addr)
    if return_addr != 'formsHome' :
        del request.session['form_return_redirect']
        request.session.modified = True
    
    if formID and Form.objects.filter(id=formID).exists() :
        formToDelete = Form.objects.get(pk=formID)
        if request.user.is_authenticated and formToDelete.canEdit(request.user) :
            questionFormsRelations = QuestionsForm.objects.filter(formid_form=formID)
            for questionFormsRelation in questionFormsRelations:
                questionFormsRelation.delete()

            formToDelete.delete()

    return redirect(return_addr)


def createQuestion(request, questionID=None,formID=None):
    questionCreate = None
    errorMessage = None
    questionCreation_form = None
    optionsInputed = []
    #formCreation_form = openEndedQuestionCreation(currentUser=request.user, associatedForm=None, questionToEdit=None)

    if questionID and Questions.objects.filter(id=questionID).exists():
        questionToEdit = Questions.objects.get(pk=questionID)
        if not questionToEdit.canEdit(request.user) :
            errorMessage = "Erro: Utilizador não pode editar esta questão"
    elif request.user.groups.filter(pk=2).exists():
        errorMessage = "Erro: Participante não pode criar questões, a conta deve ser do tipo Proponente ou Administrator"

    if formID and Form.objects.filter(id=formID).exists():
        formToEdit = Form.objects.get(pk=formID)
        if not formToEdit.canEdit(request.user):
            errorMessage = "Erro: Utilizador não pode editar este formulário"

    if not questionID or not Questions.objects.filter(id=questionID).exists() :
        questionCreate = True


    

    if not errorMessage :
        if questionID and Questions.objects.filter(id=questionID).exists() :
            questionToEdit = Questions.objects.get(id=questionID)
        else :
            questionToEdit = None
        
        if formID or Form.objects.filter(id=formID).exists() :
            associatedForm = Form.objects.get(id=formID)
        else :
            associatedForm = None

        if request.method == 'POST':
            questionCreation_form = openEndedQuestionCreation(request.POST, currentUser=request.user, associatedForm=associatedForm, questionToEdit=questionToEdit)

            optionCount = 0
            while (request.POST.get("option"+str(optionCount),None)) :
                optionsInputed.append(request.POST.get("option"+str(optionCount),None))
                optionCount = optionCount + 1

            if questionCreation_form.is_valid():
                newForm = questionCreation_form.save()
                                    
                newForm.setAllOptions(optionsInputed, request.user)

                if associatedForm :
                    return redirect("checkFormLayout", associatedForm.id)
                else :
                    return redirect("listQuestions")

        else:
            if questionToEdit :
                questionCreation_form = openEndedQuestionCreation(currentUser=request.user, associatedForm=associatedForm, questionToEdit=questionToEdit,initial={
                    'question': questionToEdit.question, 'required': questionToEdit.required, 'questionType': questionToEdit.questiontypeid_questiontype.id
                })
                for option in questionToEdit.options :
                    optionsInputed.append(option.option)
            else :
                questionCreation_form = openEndedQuestionCreation(currentUser=request.user, associatedForm=associatedForm, questionToEdit=questionToEdit)

    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"

    cancelRedirect = request.session.get("createQuestion_cancelRedirect", None)
    template = loader.get_template('template_create_new_question.html')
    context = {
        'questionCreate' : questionCreate,
        'options' : optionsInputed,
        'errorMessage' : errorMessage,
        'questionCreation' : questionCreation_form,
        'cancelRedirect' : cancelRedirect
    }
    return HttpResponse(template.render(context, request))


def listQuestions(request, formID=None, filterKey = None) :
    questions = None
    errorMessage = None
    formToAssociate = None

    if formID and Form.objects.filter(id=formID).exists() :
        formToAssociate = Form.objects.get(id=formID)
        if not formToAssociate.canEdit(request.user) :
            formToAssociate = None

    

    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"
    else :
        questions = Questions.objects.all()
        if not questions :
            errorMessage = "Erro: Nenhum questão existente"
        elif formToAssociate :
            questions_ = [x.id for x in questions if formToAssociate.canAssociateQuestion(x)]
            questions = Questions.objects.filter(id__in=questions_)
        
        if request.session.get("deleteOption_form_redirect") :
            del request.session["deleteOption_form_redirect"]
        if request.session.get("createOption_form_redirect") :
            del request.session["createOption_form_redirect"]
        request.session.modified = True
    request.session["form_return_redirect"] = "/forms/listquestions/"
    filterOptions = Questions.getFilterOptions()
    questionTypes = Questiontype.objects.all()

    if questions :
        questions = Questions.sortByKey(questions, filterKey)
        for question in questions :
            question.canEdit = question.canEdit(request.user)
            question.canDuplicate = question.canDuplicate(request.user)

    if formID != None :
        if filterKey :
            request.session["createQuestion_cancelRedirect"] = reverse('listQuestions', args =[formID, filterKey])
            request.session["createOption_cancelRedirect"] = reverse('listQuestions', args =[formID, filterKey])
        else :
            request.session["createQuestion_cancelRedirect"] = reverse('listQuestions', args =[formID])
            request.session["createOption_cancelRedirect"] = reverse('listQuestions', args =[formID])
    else :
        request.session["createQuestion_cancelRedirect"] = reverse('listQuestions')
        request.session["createOption_cancelRedirect"] = reverse('listQuestions')
    
    template = loader.get_template('template_list_questions.html')
    context = {
        'filterOptions' : filterOptions,
        'questionTypes' : questionTypes,
        'errorMessage' : errorMessage,
        'questions' : questions,
        'formToAssociate' : formToAssociate,
        'filterKey' : filterKey,
    }
    return HttpResponse(template.render(context, request))


def associateQuestion(request, questionID=None, formID=None) :
    if questionID and Questions.objects.filter(id=questionID).exists() :
        question = Questions.objects.get(id=questionID)
    else :
        return redirect('listQuestions')

    if formID and Form.objects.filter(id=formID).exists() :
        form = Form.objects.get(id=formID)
    else :
        return redirect('listQuestions')

    form.associateQuestion(question, request.user)

    return redirect('listQuestions', form.id)

def deassociateQuestion(request, questionID=None, formID=None) :
    if questionID and Questions.objects.filter(id=questionID).exists() :
        question = Questions.objects.get(id=questionID)
    else :
        return redirect('checkFormLayout')

    if formID and Form.objects.filter(id=formID).exists() :
        form = Form.objects.get(id=formID)
    else :
        return redirect('checkFormLayout')

    form.deassociateQuestion(question, request.user)

    return redirect('checkFormLayout', form.id)

def createOption(request, questionID=None, optionID=None) :
    optionCreate = None
    errorMessage = None
    optionCreation_form = None
    #formCreation_form = openEndedQuestionCreation(currentUser=request.user, associatedForm=None, questionToEdit=None)

    if questionID and Questions.objects.filter(id=questionID).exists():
        questionToEdit = Questions.objects.get(pk=questionID)
        if not questionToEdit.canEdit(request.user) :
            errorMessage = "Erro: Utilizador não pode editar esta questão"

    if not optionID or not Multipleoptions.objects.filter(id=optionID).exists() :
        optionCreate = True

    if not errorMessage :
        optionToEdit = None
        if optionID and Multipleoptions.objects.filter(id=optionID).exists() :
            optionToEdit = Multipleoptions.objects.get(id=optionID)
            
        associatedQuestion = Questions.objects.get(id=questionID)

        if request.method == 'POST':
            optionCreation_form = QuestionOptionForm(request.POST, currentUser=request.user, associatedQuestion=associatedQuestion, optionToEdit=optionToEdit)
            if optionCreation_form.is_valid():
                newOption = optionCreation_form.save()

                if newOption and request.session.get('createOption_form_redirect', None) :
                    return redirect("checkFormLayout", request.session.get('createOption_form_redirect', None))
                else :
                    return redirect("listQuestions")

        else:
            if optionToEdit :
                optionCreation_form = QuestionOptionForm(currentUser=request.user, associatedQuestion=associatedQuestion, optionToEdit=optionToEdit,initial={
                    'option': optionToEdit.option,
                })
            else :
                optionCreation_form = QuestionOptionForm(currentUser=request.user, associatedQuestion=associatedQuestion, optionToEdit=optionToEdit)

    if request.user.groups.filter(id=2).exists() :
        errorMessage = "Erro: Utilizador não possui acesso a esta pagina"

    cancelRedirect = request.session.get("createOption_cancelRedirect", None)
    template = loader.get_template('template_create_new_option.html')
    context = {
        'optionCreate' : optionCreate,
        'errorMessage' : errorMessage,
        'optionCreation' : optionCreation_form,
        'cancelRedirect' : cancelRedirect
    }
    return HttpResponse(template.render(context, request))

def deleteOption(request, questionID=None, optionID=None) :
    expression = not questionID or not Questions.objects.filter(id=questionID)
    expression = expression or not optionID or not Multipleoptions.objects.filter(id=optionID)
    
    if not expression :
        question = Questions.objects.get(id=questionID)
        option = Multipleoptions.objects.get(id=optionID)
        expression = question.canEdit(request.user)
        expression = expression and option.questionsid_questions == question
        if expression :
            option.delete()
            question.notifyOptionRemoval(request.user)

    if request.session.get('deleteOption_form_redirect', None) : 
        return redirect("checkFormLayout", request.session.get('deleteOption_form_redirect', None))
    else :
        return redirect("listQuestions")

def deleteQuestion(request, questionID=None) :
    questionToDelete = None
    if questionID and Questions.objects.filter(id=questionID).exists() :
        questionToDelete = Questions.objects.get(id=questionID)
    
    if questionToDelete and questionToDelete.canEdit(request.user):
        forms_questions = QuestionsForm.objects.filter(questionsid_questions=questionToDelete)
        for forms_question in forms_questions :
            forms_question.delete()
        
        for option in questionToDelete.options :
            option.delete()
        
        for answer in questionToDelete.allanswers :
            answer.delete()
        questionToDelete.delete()
        


    return redirect("listQuestions")


def duplicateForm(request, formID=None) :
    if formID and Form.objects.filter(id=formID).exists() :
        formToDuplicate = Form.objects.get(id=formID)
        if formToDuplicate.canDuplicate(request.user) :
            newForm = formToDuplicate.duplicate(request.user)
            return redirect('checkFormLayout', newForm.id)
        return redirect('listFormsFromType', formToDuplicate.formtypeid_formtype)
    return redirect('formsHome')

def duplicateQuestion(request, questionID=None) :
    if questionID and Questions.objects.filter(id=questionID).exists() :
        questionToDuplicate = Questions.objects.get(id=questionID)
        if questionToDuplicate.canDuplicate(request.user) :
            newQuestion = questionToDuplicate.duplicate(request.user)
            return redirect('createQuestion', newQuestion.id, 0)
        return redirect('listQuestions')
    return redirect('formsHome')

def publishForm(request, formID=None) :
    if formID and Form.objects.filter(id=formID).exists() :
        formToPublish = Form.objects.get(id=formID)
        if formToPublish.canPublish(request.user) :
            formToPublish.publish(request.user)
            return redirect(request.session.get('publishForm_form_redirect', '/forms/checkformlayout/' + str(formToPublish.id) + '/'))
        return redirect('listFormsFromType', formToDuplicate.formtypeid_formtype)
    return redirect('formsHome')

def archiveForm(request, formID=None) :
    if formID and Form.objects.filter(id=formID).exists() :
        formToArchive = Form.objects.get(id=formID)
        if formToArchive.canArchive(request.user) :
            formToArchive.archive(request.user)
            return redirect(request.session.get('archiveForm_form_redirect', '/forms/checkformlayout/' + str(formToArchive.id) + '/'))
        return redirect('listFormsFromType', formToDuplicate.formtypeid_formtype)
    return redirect('formsHome')

def unarchiveForm(request, formID=None) :
    if formID and Form.objects.filter(id=formID).exists() :
        formToArchive = Form.objects.get(id=formID)
        if formToArchive.canUnarchive(request.user) :
            formToArchive.unarchive(request.user)
            return redirect(request.session.get('archiveForm_form_redirect', '/forms/checkformlayout/' + str(formToArchive.id) + '/'))
        return redirect('listFormsFromType', formToDuplicate.formtypeid_formtype)
    return redirect('formsHome')
    

def testForm(request, formID = 1):
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