# Generated by Django 3.2 on 2021-04-27 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AssetManagement', '0001_initial'),
        ('Models', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('day', models.DateField(db_column='Day')),
            ],
            options={
                'db_table': 'day',
            },
        ),
        migrations.CreateModel(
            name='Timebracket',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('starttime', models.TimeField(db_column='StartTime')),
                ('endtime', models.TimeField(db_column='EndTime')),
                ('asset_logisticsid', models.ForeignKey(blank=True, db_column='Asset_logisticsID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Models.assetlogistics')),
                ('assetid', models.ForeignKey(blank=True, db_column='AssetID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.asset')),
                ('dayid_day', models.ForeignKey(db_column='DayID_Day', on_delete=django.db.models.deletion.DO_NOTHING, to='Schedules.day')),
            ],
            options={
                'db_table': 'timebracket',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('eventid', models.ForeignKey(db_column='EventID', on_delete=django.db.models.deletion.DO_NOTHING, to='Models.event')),
            ],
            options={
                'db_table': 'schedule',
            },
        ),
        migrations.AddField(
            model_name='day',
            name='scheduleid_schedule',
            field=models.ForeignKey(db_column='ScheduleID_Schedule', on_delete=django.db.models.deletion.DO_NOTHING, to='Schedules.schedule'),
        ),
    ]
