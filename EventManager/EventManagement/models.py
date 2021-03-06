from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PreEventManagement.models import Event
from FormManagement.models import *


class Resgistration(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('PreEventManagement.Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    dateofregistration = models.DateTimeField(db_column='dateOfRegistration')  # Field name made lowercase.
    waspresent = models.BooleanField(db_column='WasPresent', default=False)  # Field name made lowercase.
    participantuserid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='ParticipantUserID')  # Field name made lowercase.
    state=models.IntegerField(db_column='state',default=0)
 


    def canCancel(self, user) :
        return (user == self.participantuserid or user.groups.filter(pk=1).exists()) and self.waspresent != True

    @staticmethod
    def canRegister(event, user) :
        return not Resgistration.objects.filter(participantuserid=user, eventid_event=event).exists()

    

    def cancelregistrations(self, user) :
        if self.canCancel(user)  :
            Answer.objects.filter(resgistrationid=self.id).delete()
            self.delete()

    def changeCheckoutStatus(self, newStatus) :
        self.waspresent = newStatus
        self.save()
        return self.waspresent

    def changevalidateStatus(self, newStatus) :
        self.state = newStatus
        self.save()
        return self.state

    #to be implemented
    def canCancelCheckout(self, user) :
        return True
    
    @staticmethod
    def sortByKey(setToSort, key) :
        if( not setToSort ) :
            return None
        
        if key :
            if key.find("00") > -1 :
                return setToSort.order_by("eventid_event")
            if key.find("01") > -1 :
                return setToSort.order_by("-eventid_event")
            if key.find("10") > -1 :
                return setToSort.order_by("dateofregistration")
            if key.find("11") > -1 :
                return setToSort.order_by("-dateofregistration")
            if key.find("20") > -1 :
                return setToSort.order_by("waspresent")
            if key.find("21") > -1 :
                return setToSort.order_by("-waspresent")
            if key.find("30") > -1 :
                return setToSort.order_by("participantuserid")
            if key.find("31") > -1 :
                return setToSort.order_by("-participantuserid")
            if key.find("40") > -1 :
                return setToSort.order_by("state")
            if key.find("41") > -1 :
                return setToSort.order_by("-state")
                
        return setToSort.order_by("participantuserid") 


    class Meta:
        db_table = 'resgistration'