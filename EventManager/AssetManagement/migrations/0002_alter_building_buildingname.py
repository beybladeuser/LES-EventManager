# Generated by Django 3.2 on 2021-04-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AssetManagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='buildingname',
            field=models.CharField(db_column='BuildingName', max_length=255),
        ),
    ]
