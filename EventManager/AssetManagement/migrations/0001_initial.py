# Generated by Django 3.2 on 2021-04-26 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('assetname', models.CharField(db_column='AssetName', max_length=255, unique=True)),
                ('quantity', models.IntegerField(db_column='Quantity')),
            ],
            options={
                'db_table': 'asset',
            },
        ),
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('campusname', models.CharField(db_column='CampusName', max_length=255, unique=True)),
            ],
            options={
                'db_table': 'campus',
            },
        ),
        migrations.CreateModel(
            name='Equipmenttype',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('typename', models.CharField(db_column='TypeName', max_length=255, unique=True)),
            ],
            options={
                'db_table': 'equipmenttype',
            },
        ),
        migrations.CreateModel(
            name='Servicetype',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('typename', models.CharField(db_column='TypeName', max_length=255, unique=True)),
            ],
            options={
                'db_table': 'servicetype',
            },
        ),
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('buildingname', models.CharField(db_column='BuildingName', max_length=255, unique=True)),
                ('campusid', models.ForeignKey(db_column='CampusID', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.campus')),
            ],
            options={
                'db_table': 'building',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('assetid', models.OneToOneField(db_column='AssetID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='AssetManagement.asset')),
                ('servicetypeid_servicetype', models.ForeignKey(db_column='ServiceTypeID_ServiceType', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.servicetype')),
            ],
            options={
                'db_table': 'service',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('assetid', models.OneToOneField(db_column='AssetID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='AssetManagement.asset')),
                ('buildingid_building', models.ForeignKey(db_column='BuildingID_Building', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.building')),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('assetid', models.OneToOneField(db_column='AssetID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='AssetManagement.asset')),
                ('equipmenttypeid_equipmenttype', models.ForeignKey(db_column='EquipmentTypeID_EquipmentType', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.equipmenttype')),
            ],
            options={
                'db_table': 'equipment',
            },
        ),
    ]
