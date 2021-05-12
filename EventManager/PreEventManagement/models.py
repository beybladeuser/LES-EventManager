from django.db import models, connection
from django.contrib.auth.models import User
from django.conf import settings


from FormManagement.models import *
from AssetManagement.models import *
from Sessions.models import *

# Create your models here.
class AssetEvent(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    assetid_asset = models.ForeignKey('AssetManagement.Asset', models.DO_NOTHING, db_column='AssetID_Asset')  # Field name made lowercase.
    eventid_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.

    class Meta:
        
        db_table = 'asset_event'


class AssetLogistics(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    servicetypeid_servicetype = models.ForeignKey('AssetManagement.Servicetype', models.DO_NOTHING, db_column='ServiceTypeID_ServiceType', blank=True, null=True)  # Field name made lowercase.
    equipmenttypeid_equipmenttype = models.ForeignKey('AssetManagement.Equipmenttype', models.DO_NOTHING, db_column='EquipmentTypeID_EquipmentType', blank=True, null=True)  # Field name made lowercase.
    seats = models.IntegerField(db_column='Seats', blank=True, null=True)  # Field name made lowercase.
    seatsforreducedmobility = models.IntegerField(db_column='SeatsForReducedMobility', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.

    class Meta:
        
        db_table = 'asset_logistics'

class Event(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventtypeid = models.ForeignKey('Eventtype', models.DO_NOTHING, db_column='EventTypeID')  # Field name made lowercase.
    formproposalid = models.ForeignKey('FormManagement.Form', models.DO_NOTHING, db_column='FormProposalID', related_name='Event2proposalForm')
    formresgistrationid = models.ForeignKey('FormManagement.Form', models.DO_NOTHING, db_column='FormResgistrationID', related_name='Event2registerForm')  # Field name made lowercase.
    formfeedbackid = models.ForeignKey('FormManagement.Form', models.DO_NOTHING, db_column='FormFeedBackID', related_name='Event2feedbackForm')  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.
    wasvalidated = models.TextField(db_column='wasValidated')  # Field name made lowercase. This field type is a guess.
    proponentid = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='ProponentID')  # Field name made lowercase.
    eventname = models.CharField(db_column='eventName', max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'event'


class Eventtype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=255)  # Field name made lowercase.

    @staticmethod
    def makeOptions() :
        if "eventtype" in connection.introspection.table_names() :
            eventTypes = Eventtype.objects.all()
            options=([(eventType.id, eventType.typename) for eventType in eventTypes])
            return options
        else:
            return (("1", "No Database created"),)

    class Meta:
        
        db_table = 'eventtype'