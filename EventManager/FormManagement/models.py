#criar form temos que dizer que tipo de form que é
#so pode haver um formulario para cada tipo de evento
#feed back e inscriçao é ilimitado
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from Models.models import *


class Answer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    questionsid_questions = models.ForeignKey('Questions', models.DO_NOTHING, db_column='QuestionsID_Questions')  # Field name made lowercase.
    eventid_event = models.ForeignKey('Models.Event', models.DO_NOTHING, db_column='EventID_Event', blank=True, null=True)  # Field name made lowercase.
    resgistrationid = models.ForeignKey('Models.Resgistration', models.DO_NOTHING, db_column='ResgistrationID', blank=True, null=True)  # Field name made lowercase.
    answer = models.CharField(max_length=255)
    dateofcreation = models.DateTimeField(db_column='DateOfCreation')  # Field name made lowercase.

    def __str__(self) :
        return "Q: " + self.questionsid_questions.question + " | A: " + self.answer

    def getUserThatAnsweredThis(self) :
        authUser = None
        associatedResgistration = self.resgistrationid
        if associatedResgistration :
            userID = associatedResgistration.participantuserid.utilizador_ptr_id
            authUser = User.objects.get(pk=userID)
        return authUser

    usersThatAnsweredThis = property(getUserThatAnsweredThis)

    class Meta:
        managed = True
        db_table = 'answer'

# Create your models here.
class Form(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventtypeid = models.ForeignKey('Models.Eventtype', models.DO_NOTHING, db_column='EventTypeID')  # Field name made lowercase.
    formtypeid_formtype = models.ForeignKey('Formtype', models.DO_NOTHING, db_column='FormTypeID_FormType')  # Field name made lowercase.
    formname = models.CharField(db_column='FormName', max_length=255)  # Field name made lowercase.
    dateofcreation = models.DateTimeField(db_column='DateOfCreation')  # Field name made lowercase.
    dateoflastedit = models.DateTimeField(db_column='DateOfLastEdit')  # Field name made lowercase.
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='CreatedBy', related_name='FormCreatedBy')
    lasteditedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='LastEditedBy', related_name='FormLastEditedBy')

    def __str__(self) :
        return self.formname

    def getFormType(self) :
        return self.formtypeid_formtype.typename

    def getEventType(self) :
        return self.eventtypeid.typename

    def getQuestions(self) :
        Form_Questions = QuestionsForm.objects.filter(formid_form=self.id)
        Questions_Associated_with_form = [x.questionsid_questions for x in Form_Questions]
        return Questions_Associated_with_form

    formquestions = property(getQuestions)

    class Meta:
        managed = True
        db_table = 'form'


class Formtype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=255)  # Field name made lowercase.

    def __str__(self) :
        return self.typename

    @staticmethod
    def makeOptions() :
        formTypes = Formtype.objects.all()
        options=([(formType.id, formType.typename) for formType in formTypes])
        return options

    

    class Meta:
        managed = True
        db_table = 'formtype'


class Questions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    questiontypeid_questiontype = models.ForeignKey('Questiontype', models.DO_NOTHING, db_column='QuestionTypeID_QuestionType')  # Field name made lowercase.
    question = models.CharField(max_length=255)
    
    dateofcreation = models.DateTimeField(db_column='DateOfCreation')  # Field name made lowercase.
    dateoflastedit = models.DateTimeField(db_column='DateOfLastEdit')  # Field name made lowercase.
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='CreatedBy', related_name='QuestionCreatedBy')
    lasteditedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='LastEditedBy', related_name='QuestionLastEditedBy')

    def __str__(self) :
        return "Q: " + self.question

    def getQuestionType(self) :
        return self.questiontypeid_questiontype.typename

    def getMultipleOptions(self) :
        Options = Multipleoptions.objects.filter(questionsid_questions=self.id)
        return Options
    
    def getAllAnswers(self) :
        return Answer.objects.filter(questionsid_questions=self.id)
    

    options = property(getMultipleOptions)

    allanswers = property(getAllAnswers)

    class Meta:
        managed = True
        db_table = 'questions'

class QuestionsForm(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    questionsid_questions = models.ForeignKey('Questions', models.DO_NOTHING, db_column='QuestionsID_Questions')  # Field name made lowercase.
    formid_form = models.ForeignKey('Form', models.DO_NOTHING, db_column='FormID_Form')  # Field name made lowercase.

    def __str__(self) :
        return "Form: " + self.formid_form.formname + " | Q: " + self.questionsid_questions.question

    class Meta:
        managed = True
        db_table = 'questions_form'


class Questiontype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=255)  # Field name made lowercase.

    def __str__(self) :
        return self.typename

    class Meta:
        managed = True
        db_table = 'questiontype'

class Multipleoptions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    questionsid_questions = models.ForeignKey('Questions', models.DO_NOTHING, db_column='QuestionsID_Questions')  # Field name made lowercase.
    option = models.CharField(db_column='Option', max_length=255)  # Field name made lowercase.

    def __str__(self) :
        return "Q: " + self.questionsid_questions.question + " | Option: " + self.option

    class Meta:
        managed = True
        db_table = 'multipleoptions'