from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from PreEventManagement.models import *

# Create your models here.
class Resgistration(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    waspresent = models.IntegerField(db_column='WasPresent', blank=True, null=True)  # Field name made lowercase.
    participantuserid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='ParticipantUserID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'resgistration'