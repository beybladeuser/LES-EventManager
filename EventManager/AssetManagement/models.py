# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from Models.models import *
import datetime

class Asset(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    assetname = models.CharField(db_column='AssetName', unique=True, max_length=255)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.


    def getServiceTypeName(self):
        result = None
        service = Service.objects.filter(assetid=self.id)
        if service :
            result = service[0].servicetypeid_servicetype.typename
        return result

    service_subclass_typeName = property(getServiceTypeName)

    def __str__(self):
        return self.assetname

    def addAsset(self, )



    class Meta:
        db_table = 'asset'


class Building(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    campusid = models.ForeignKey('Campus', models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.
    buildingname = models.CharField(db_column='BuildingName', max_length=255)  # Field name made lowercase.

    def __str__(self):
       return self.buildingname

    class Meta:
        
        db_table = 'building'


class Campus(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    campusname = models.CharField(db_column='CampusName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'campus'

    def __str__(self):
       return self.campusname

    

class Equipment(models.Model):
    assetid = models.OneToOneField(Asset, models.DO_NOTHING, db_column='AssetID', primary_key=True)  # Field name made lowercase.
    equipmenttypeid_equipmenttype = models.ForeignKey('Equipmenttype', models.DO_NOTHING, db_column='EquipmentTypeID_EquipmentType')  # Field name made lowercase.

    class Meta:
        db_table = 'equipment'
      
 




class Equipmenttype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'equipmenttype'
    
    def __str__(self):
       return self.typename




class Rooms(models.Model):
    assetid = models.OneToOneField(Asset, models.DO_NOTHING, db_column='AssetID', primary_key=True)  # Field name made lowercase.
    buildingid_building = models.ForeignKey(Building, models.DO_NOTHING, db_column='BuildingID_Building')  # Field name made lowercase.

    class Meta:
        
        db_table = 'rooms'

    def __str__(self):
       return self.assetid


class Service(models.Model):
    assetid = models.OneToOneField(Asset, models.DO_NOTHING, db_column='AssetID', primary_key=True)  # Field name made lowercase.
    servicetypeid_servicetype = models.ForeignKey('Servicetype', models.DO_NOTHING, db_column='ServiceTypeID_ServiceType')  # Field name made lowercase.

    class Meta:
        
        db_table = 'service'
    
    def __str__(self):
       return self.assetid




class Servicetype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        
        db_table = 'servicetype'

    def __str__(self):
       return self.typename
    