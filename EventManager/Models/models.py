# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from FormManagement.models import *
from AssetManagement.models import *
from Sessions.models import *


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
    formresgistrationid = models.ForeignKey('FormManagement.Form', models.DO_NOTHING, db_column='FormResgistrationID', related_name='Event2registerForm')  # Field name made lowercase.
    formfeedbackid = models.ForeignKey('FormManagement.Form', models.DO_NOTHING, db_column='FormFeedBackID', related_name='Event2feedbackForm')  # Field name made lowercase.
    campusid = models.ForeignKey(Campus, models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.
    wasvalidated = models.TextField(db_column='wasValidated')  # Field name made lowercase. This field type is a guess.
    proponentid = models.ForeignKey('Sessions.Utilizador', models.DO_NOTHING, db_column='ProponentID')  # Field name made lowercase.
    eventname = models.CharField(db_column='eventName', max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'event'


class Eventtype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'eventtype'


class Informacaomensagem(models.Model):
    data = models.DateTimeField()
    pendente = models.IntegerField()
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    lido = models.IntegerField()
    emissorid = models.IntegerField(blank=True, null=True)
    recetorid = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'informacaomensagem'


class Informacaonotificacao(models.Model):
    data = models.DateTimeField()
    pendente = models.IntegerField()
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    lido = models.IntegerField()
    emissorid = models.IntegerField(blank=True, null=True)
    recetorid = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'informacaonotificacao'


class Mensagemenviada(models.Model):
    mensagem_id = models.IntegerField()

    class Meta:
        
        db_table = 'mensagemenviada'


class Mensagemrecebida(models.Model):
    mensagem_id = models.IntegerField()

    class Meta:
        
        db_table = 'mensagemrecebida'


class Notificacao(models.Model):
    level = models.CharField(max_length=20)
    unread = models.IntegerField()
    actor_object_id = models.CharField(max_length=255)
    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    action_object_object_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField()
    public = models.IntegerField()
    deleted = models.IntegerField()
    emailed = models.IntegerField()
    data = models.TextField(blank=True, null=True)
    titulo = models.CharField(max_length=255)
    descricao = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    action_object_content_type_id = models.IntegerField(blank=True, null=True)
    actor_content_type_id = models.IntegerField()
    recipient_id = models.IntegerField()
    target_content_type_id = models.IntegerField(blank=True, null=True)

    class Meta:
        
        db_table = 'notificacao'


class Resgistration(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid_event = models.ForeignKey('Event', models.DO_NOTHING, db_column='EventID_Event')  # Field name made lowercase.
    date = models.IntegerField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    waspresent = models.IntegerField(db_column='WasPresent', blank=True, null=True)  # Field name made lowercase.
    participantuserid = models.ForeignKey(Participante, models.DO_NOTHING, db_column='ParticipantUserID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'resgistration'



