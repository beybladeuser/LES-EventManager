# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection
from django.contrib.auth.models import User
from django.conf import settings
from Models.models import *
import datetime

class Asset(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    assetname = models.CharField(db_column='AssetName', max_length=255)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    canAdd = False






    def delete_asset(self):        
        if Service.objects.filter(assetid=self.id).exists():
            service = Service.objects.get(assetid=self.id)
            service.delete()
        elif Equipment.objects.filter(assetid=self.id).exists():
            equipment = Equipment.objects.get(assetid=self.id)
            equipment.delete()
        elif Rooms.objects.filter(assetid=self.id).exists():
            room = Rooms.objects.get(assetid=self.id)
            room.delete()
        
        self.delete()
        
    def userHasEditPermitions(self, user) :
        return (user.id == self.createdby.id or user.groups.filter(pk=1).exists())


    def getServiceType(self):
        result = None
        service = Service.objects.filter(assetid=self.id)
        if service :
            result = service[0].servicetypeid_servicetype.typename
        return result

    service_subclass_type = property(getServiceType)

    def getEquipmentType(self):
        result = None
        equipment = Equipment.objects.filter(assetid=self.id)
       
        if equipment:
            result = equipment[0].equipmenttypeid_equipmenttype.typename
        return result

    def getRoom(self):
        result = None
        room = Rooms.objects.filter(assetid=self.id)
        if room  :
            result = room[0]
        return result


    def __str__(self):
        return self.assetname
        

    class Meta:
        db_table = 'asset'



class Building(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    campusid = models.ForeignKey('Campus', models.DO_NOTHING, db_column='CampusID')  # Field name made lowercase.
    buildingname = models.CharField(db_column='BuildingName', max_length=255)  # Field name made lowercase.


    def building_getCampus(self):
        return self.campusid


    def building_getCampusName(self):
        result = None      
        campus = Building.objects.filter(id=campusid)
        if campus :
            result = campus[0].campusname
        return result   



    def CampusName_BuildingName(self):
        return str(self.campusid)  + " - " + self.buildingname



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
      
    def __str__(self):
       return self.assetid




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

    def room_GetBuilding(self):
        return self.buildingid_building

    
    class Meta:
        db_table = 'rooms'

    # def __str__(self):
    #    return self.assetid + " - " + self.buildingid_building


class Service(models.Model):
    assetid = models.OneToOneField(Asset, models.DO_NOTHING, db_column='AssetID', primary_key=True)  # Field name made lowercase.
    servicetypeid_servicetype = models.ForeignKey('Servicetype', models.DO_NOTHING, db_column='ServiceTypeID_ServiceType')  # Field name made lowercase.

    class Meta:
        db_table = 'service'
    
    def __str__(self):
       return self.assetid
     
    @staticmethod
    def makeOptions():
        if "servicetype" in connection.introspection.table_names():
            servicetypes = Servicetype.objects.all()
            options=([(servicetype.id, servicetype.typename) for servicetype in servicetypes])
            return options
        else:
            return (("1", "No Database created"),)



class Servicetype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'servicetype'

    def __str__(self):
       return self.typename
    