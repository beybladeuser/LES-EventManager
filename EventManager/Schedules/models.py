from django.db import models
from PreEventManagement.models import *

# Create your models here.
class Day(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    scheduleid_schedule = models.ForeignKey('Schedule', models.DO_NOTHING, db_column='ScheduleID_Schedule')  # Field name made lowercase.
    day = models.DateField(db_column='Day')  # Field name made lowercase.

    class Meta:
        
        db_table = 'day'

class Schedule(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    eventid = models.ForeignKey('PreEventManagement.Event', models.DO_NOTHING, db_column='EventID')  # Field name made lowercase.

    class Meta:
        
        db_table = 'schedule'

class Timebracket(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    assetid = models.ForeignKey('AssetManagement.Asset', models.DO_NOTHING, db_column='AssetID', blank=True, null=True)  # Field name made lowercase.
    asset_logisticsid = models.ForeignKey('PreEventManagement.AssetLogistics', models.DO_NOTHING, db_column='Asset_logisticsID', blank=True, null=True)  # Field name made lowercase.
    dayid_day = models.ForeignKey('Day', models.DO_NOTHING, db_column='DayID_Day')  # Field name made lowercase.
    starttime = models.TimeField(db_column='StartTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='EndTime')  # Field name made lowercase.

    class Meta:
        
        db_table = 'timebracket'