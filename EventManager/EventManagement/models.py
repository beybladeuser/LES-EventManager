from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from PreEventManagement.models import *
from FormManagement.models import *


class Resgistration(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('PreEventManagement.Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    dateofregistration = models.DateTimeField(db_column='dateOfRegistration')  # Field name made lowercase.
    waspresent = models.BooleanField(db_column='WasPresent', default=False)  # Field name made lowercase.
    participantuserid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='ParticipantUserID')  # Field name made lowercase.

    def cancelregistrations(self, user) :
        Answer.objects.filter(resgistrationid=self.id).delete()
        return True

   

    class Meta:
        db_table = 'resgistration'