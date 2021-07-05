#criar form temos que dizer que tipo de form que é
#so pode haver um formulario para cada tipo de evento
#feed back e inscriçao é ilimitado
from django.db import models, connection
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from PreEventManagement.models import *

import datetime
import re



class Answer(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    associatedformid = models.ForeignKey('Form', models.DO_NOTHING, db_column='AssociatedFormID', default=1)
    questionsid_questions = models.ForeignKey('Questions', models.DO_NOTHING, db_column='QuestionsID_Questions')  # Field name made lowercase.
    eventid_event = models.ForeignKey('PreEventManagement.Event', models.DO_NOTHING, db_column='EventID_Event', blank=True, null=True)  # Field name made lowercase.
    resgistrationid = models.ForeignKey('EventManagement.Resgistration', models.DO_NOTHING, db_column='ResgistrationID', blank=True, null=True)  # Field name made lowercase.
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
    eventtypeid = models.ForeignKey('PreEventManagement.Eventtype', models.DO_NOTHING, db_column='EventTypeID')  # Field name made lowercase.
    formtypeid_formtype = models.ForeignKey('Formtype', models.DO_NOTHING, db_column='FormTypeID_FormType')  # Field name made lowercase.
    formname = models.CharField(db_column='FormName', max_length=255)  # Field name made lowercase.
    dateofcreation = models.DateTimeField(db_column='DateOfCreation')  # Field name made lowercase.
    dateoflastedit = models.DateTimeField(db_column='DateOfLastEdit')  # Field name made lowercase.
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='CreatedBy', related_name='FormCreatedBy')
    lasteditedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='LastEditedBy', related_name='FormLastEditedBy')
    published = models.BooleanField(db_column='published', default=False)
    archived = models.BooleanField(db_column='Archived', default=False)

    canEdit = False
    canDuplicate = False
    
    def __str__(self) :
        return self.formname

    def getFormType(self) :
        return self.formtypeid_formtype.typename

    def getEventType(self) :
        return self.eventtypeid.typename

    def getQuestions(self) :
        Form_Questions = QuestionsForm.objects.filter(formid_form=self.id)
        Questions_Associated_with_form = [x.questionsid_questions.id for x in Form_Questions]
        return Questions.objects.filter(id__in=Questions_Associated_with_form)

    def associateQuestion(self, question, user) :
        if self.canEdit(user) :
            if self.canAssociateQuestion(question):
                form_question_association = QuestionsForm()
                form_question_association.questionsid_questions = question
                form_question_association.formid_form = self
                form_question_association.save()
                self.dateoflastedit = datetime.datetime.now()
                self.lasteditedby = user
                self.save()

    def deassociateQuestion(self, question, user) :
        if self.canEdit(user) :
            if QuestionsForm.objects.filter(questionsid_questions=question, formid_form=self):
                QuestionsForm.objects.get(questionsid_questions=question, formid_form=self).delete()
                self.dateoflastedit = datetime.datetime.now()
                self.lasteditedby = user
                self.save()

    def getAssociatedEvents(self) :
        return Event.objects.filter(Q(formproposalid=self) | Q(formresgistrationid=self) | Q(formfeedbackid=self))

    def userHasEditPermitions(self, user) :
        return (user.id == self.createdby.id or user.groups.filter(pk=1).exists())

    def wasAnswered(self) :
        for question in self.formquestions :
            for answer in question.allanswers :
                if answer.associatedformid == self :
                    return True
        
        return False
    
    def isValid(self) :
        #if self.formtypeid_formtype.id == 1 :
        #    hasRegisSelectQuestion = 0
        #    hasFeedBackSelect = 0
        #    if self.formquestions :
        #        for question in self.formquestions :
        #            if question.questiontypeid_questiontype.id == 3 :
        #                hasRegisSelectQuestion = hasRegisSelectQuestion + 1
        #            if question.questiontypeid_questiontype.id == 4 :
        #                hasFeedBackSelect = hasFeedBackSelect + 1
        #    if hasRegisSelectQuestion != 1 or hasFeedBackSelect != 1 :
        #        #lacking both regis or feedback
        #        return 1
        return 0

    def canEdit(self, user) :
        return self.userHasEditPermitions(user) and not self.archived and not self.getAssociatedEvents()

    def canDuplicate(self, user) :
        return not user.groups.filter(pk=2).exists() and self.isValid() == 0 and self.formtypeid_formtype.canCreate(user)

    def canDisplay(self, user) :
        return (user.id == self.createdby.id or user.groups.filter(pk=1).exists() or self.published) and not user.groups.filter(pk=2).exists()

    def canPublish(self, user) :
        return self.userHasEditPermitions(user) and not self.archived and len(self.formquestions) > 0 and self.isValid() == 0

    def canArchive(self, user) :
        return self.userHasEditPermitions(user) and not self.archived and len(self.formquestions) > 0 and self.isValid() == 0

    def canUnarchive(self, user) :
        return self.userHasEditPermitions(user) and user.id == self.createdby.id and self.archived

    def canAssociateQuestion(self, question) :
        e1 = not QuestionsForm.objects.filter(questionsid_questions=question, formid_form=self).exists()
        e2 = self.canAssociateQuestionType(question.questiontypeid_questiontype)
        return e1 and e2
    
    def canAssociateQuestionType(self, questionType) :
        #return not (self.formtypeid_formtype.id != 1 and (questionType.id == 3 or questionType.id == 4 or questionType.id == 5 or questionType.id == 6))
        return not (self.formtypeid_formtype.id != 1 and (questionType.id == 5 or questionType.id == 6))
    
    def duplicate(self, user) :
        result = Form()
        result.eventtypeid = self.eventtypeid
        result.formtypeid_formtype = self.formtypeid_formtype

        copyTxtList = re.findall(r" \(Copy_[0-9]+\)", self.formname)
        if (len(copyTxtList) > 0) :
            copyTxt = copyTxtList[0]
        else :
            copyTxt = ""
        name = self.formname.replace(copyTxt, '')
        name = name.replace('(', '\(')
        name = name.replace(')', '\)')
        result.formname = name + " (Copy_" + str(Form.objects.filter(formname__regex=r"^"+ name, formtypeid_formtype=self.formtypeid_formtype).count()) + ")"
        result.formname = result.formname.replace('\(', '(')
        result.formname = result.formname.replace('\)', ')')

        result.dateofcreation = datetime.datetime.now()
        result.dateoflastedit = datetime.datetime.now()
        result.createdby = user
        result.lasteditedby = user
        result.published = False
        result.archived = False

        if self.formtypeid_formtype.id == 1 :

            for form in Form.objects.filter(formtypeid_formtype=Formtype.getProposalType(), eventtypeid=self.eventtypeid) :
                form.archived = True
                form.save()


        result.save()
        for question in self.formquestions :
            result.associateQuestion(question, user)

        return result

    def publish(self, user) :
        if self.canPublish(user) :
            self.published = True
            self.save()

    def archive(self, user) :
        if self.canArchive(user) :
            self.archived = True
            self.save()

    def unarchive(self, user) :
        if self.canUnarchive(user) :
            if self.formtypeid_formtype.id == 1 :
                proposalForms = Form.objects.filter(formtypeid_formtype=self.formtypeid_formtype)
                for proposalForm in proposalForms :
                    if proposalForm.eventtypeid == self.eventtypeid :
                        proposalForm.archived = True
                        proposalForm.save()
            self.archived = False
            self.save()

    @staticmethod
    def sortByKey(setToSort, key) :
        if not setToSort:
            return None
        if key :
            if key.find("00") > -1: 
                return setToSort.order_by('formname')
            elif key.find("01") > -1:
                return setToSort.order_by('-formname')
    
            if key.find("10") > -1: 
                return setToSort.order_by('formtypeid_formtype')
            elif key.find("11") > -1:
                return setToSort.order_by('-formtypeid_formtype')
    
            if key.find("20") > -1: 
                return setToSort.order_by('eventtypeid')
            elif key.find("21") > -1:
                return setToSort.order_by('-eventtypeid')
    
            
            if key.find("30") > -1: 
                return setToSort.order_by('published')
            elif key.find("31") > -1:
                return setToSort.order_by('-published')
    
            if key.find("40") > -1: 
                return setToSort.order_by('archived')
            elif key.find("41") > -1:
                return setToSort.order_by('-archived')
    
            if key.find("50") > -1: 
                return setToSort.order_by('createdby')
            elif key.find("51") > -1:
                return setToSort.order_by('-createdby')
    
            if key.find("60") > -1: 
                return setToSort.order_by('dateofcreation')
            elif key.find("61") > -1:
                return setToSort.order_by('-dateofcreation')
    
            if key.find("70") > -1: 
                return setToSort.order_by('lasteditedby')
            elif key.find("71") > -1:
                return setToSort.order_by('-lasteditedby')
    
            if key.find("80") > -1: 
                return setToSort.order_by('dateoflastedit')
            elif key.find("81") > -1:
                return setToSort.order_by('-dateoflastedit')

        return setToSort.order_by('formname')
            




    @staticmethod
    def getFilterOptions() :
        return ("Event Type", "Creator", "Last Editor")
    

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
    def makeOptions(user) :
        if "formtype" in connection.introspection.table_names() :
            formTypes = Formtype.objects.all()
            options=([(formType.id, formType.typename) for formType in formTypes if formType.canCreate(user)])
            return options

        else:
            return (("1", "No Database created"),)

    @staticmethod
    def getProposalType() :
        if "formtype" in connection.introspection.table_names() :
            return Formtype.objects.get(id=1)
        else :
            return False

    def canCreate(self, user) :
        if (self.id == 1 and user.groups.filter(pk=1).exists()) :
            return True
        elif (self.id != 1 and not user.groups.filter(pk=2).exists()) :
            return True
        else :
            return False


    class Meta:
        managed = True
        db_table = 'formtype'


class Questions(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    questiontypeid_questiontype = models.ForeignKey('Questiontype', models.DO_NOTHING, db_column='QuestionTypeID_QuestionType')  # Field name made lowercase.
    question = models.CharField(max_length=255)
    required = models.BooleanField(db_column='Required', default=False)

    dateofcreation = models.DateTimeField(db_column='DateOfCreation')  # Field name made lowercase.
    dateoflastedit = models.DateTimeField(db_column='DateOfLastEdit')  # Field name made lowercase.
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='CreatedBy', related_name='QuestionCreatedBy')
    lasteditedby = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='LastEditedBy', related_name='QuestionLastEditedBy')

    canEdit = False
    canDuplicate = False

    def __str__(self) :
        return "Q: " + self.question

    def getQuestionType(self) :
        return self.questiontypeid_questiontype.typename

    def getMultipleOptions(self) :
        Options = Multipleoptions.objects.filter(questionsid_questions=self.id)
        return Options
    
    def getAllAnswers(self) :
        return Answer.objects.filter(questionsid_questions=self.id)

    def getAnswersForForm(self, formID) :
        return self.allanswers.filter(associatedformid=formID)

    def makeOptions(self) :
        if ("questions" and "multipleoptions") in connection.introspection.table_names() :
            options=([(option.id, option.option) for option in self.options])
            return options

        else:
            return (("1", "No Database created"),)

    def getAssociatedForms(self) :
        questionsForms = QuestionsForm.objects.filter(questionsid_questions=self)
        associatedForms = [x.formid_form for x in questionsForms]
        return associatedForms

    def userHasEditPermitions(self, user) :
        return (user.id == self.createdby.id or user.groups.filter(pk=1).exists())

    def canEdit(self, user) :
        userHasPermission = self.userHasEditPermitions(user)
        isAssociated = self.associatedforms
        expr = not self.allanswers
        #if a question only has one form associated then it can be edited
        if expr and isAssociated :
            associationsCount =len(isAssociated)
            if not (associationsCount == 1 and isAssociated[0].canEdit(user)):
                expr = False
        return userHasPermission and expr
    
    def notifyNewOption(self, user) :
        if self.questiontypeid_questiontype.id != 2 :
            multiChoiceType = Questiontype.objects.get(id=2)
            self.questiontypeid_questiontype = multiChoiceType

        self.lasteditedby = user
        self.dateoflastedit = datetime.datetime.now()
        self.save()

    def notifyOptionRemoval(self, user) :
        if not self.options :
            multiChoiceType = Questiontype.objects.get(id=1)
            self.questiontypeid_questiontype = multiChoiceType
        
        self.lasteditedby = user
        self.dateoflastedit = datetime.datetime.now()
        self.save()
        
    def canDuplicate(self, user) :
        return not user.groups.filter(pk=2).exists()

    
    def duplicate(self, user) :
        result = Questions()
        result.questiontypeid_questiontype = self.questiontypeid_questiontype
        copyTxtList = re.findall(r" \(Copy_[0-9]+\)", self.question)
        if (len(copyTxtList) > 0) :
            copyTxt = copyTxtList[0]
        else :
            copyTxt = ""
        name = self.question.replace(copyTxt, '')
        result.question = name + " (Copy_" + str(Questions.objects.filter(question__regex=r"^"+ name).count()) + ")"

        result.required = self.required
        result.archived = False

        result.dateofcreation = datetime.datetime.now()
        result.dateoflastedit = datetime.datetime.now()
        result.createdby = user
        result.lasteditedby = user

        result.save()

        for option in self.options :
            newOption = Multipleoptions()
            newOption.option = option.option
            newOption.questionsid_questions = result
            newOption.save()

        return result

    @staticmethod
    def sortByKey(setToSort, key) :
        if not setToSort:
            return None
        if key :
            if key.find("00") > -1: 
                return setToSort.order_by('question')
            elif key.find("01") > -1:
                return setToSort.order_by('-question')
    
            if key.find("10") > -1: 
                return setToSort.order_by('questiontypeid_questiontype')
            elif key.find("11") > -1:
                return setToSort.order_by('-questiontypeid_questiontype')
    
            if key.find("20") > -1: 
                return setToSort.order_by('required')
            elif key.find("21") > -1:
                return setToSort.order_by('-required')
    
            
            if key.find("30") > -1: 
                return setToSort.order_by('createdby')
            elif key.find("31") > -1:
                return setToSort.order_by('-createdby')
    
            if key.find("40") > -1: 
                return setToSort.order_by('dateofcreation')
            elif key.find("41") > -1:
                return setToSort.order_by('-dateofcreation')
    
            if key.find("50") > -1: 
                return setToSort.order_by('lasteditedby')
            elif key.find("51") > -1:
                return setToSort.order_by('-lasteditedby')
    
            if key.find("60") > -1: 
                return setToSort.order_by('dateoflastedit')
            elif key.find("61") > -1:
                return setToSort.order_by('-dateoflastedit')

        return setToSort.order_by('question')

    @staticmethod
    def getFilterOptions() :
        return ("Question Type", "Creator", "Last Editor")

    def setAllOptions(self, newOptions, user) :
        if self.canEdit(user) :
            for option in self.options :
                option.delete()
                self.notifyOptionRemoval(user)
            
            for newOption in newOptions :
                newOptionModelEntry = Multipleoptions()
                newOptionModelEntry.option = newOption
                newOptionModelEntry.questionsid_questions = self
                newOptionModelEntry.save()
                self.notifyNewOption(user)

    options = property(getMultipleOptions)

    allanswers = property(getAllAnswers)

    associatedforms = property(getAssociatedForms)

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

    @staticmethod
    def makeOptions() :
        if "questiontype" in connection.introspection.table_names() :
            questionTypes = Questiontype.objects.all()
            options=([(questionType.id, questionType.typename) for questionType in questionTypes])
            return options

        else:
            return (("1", "No Database created"),)

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