# Generated by Django 3.2 on 2021-04-26 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('FormManagement', '0001_initial'),
        ('Sessions', '__first__'),
        ('AssetManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('wasvalidated', models.TextField(db_column='wasValidated')),
                ('eventname', models.CharField(db_column='eventName', max_length=255)),
                ('campusid', models.ForeignKey(db_column='CampusID', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.campus')),
            ],
            options={
                'db_table': 'event',
            },
        ),
        migrations.CreateModel(
            name='Eventtype',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('typename', models.CharField(db_column='TypeName', max_length=255)),
            ],
            options={
                'db_table': 'eventtype',
            },
        ),
        migrations.CreateModel(
            name='Informacaomensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('pendente', models.IntegerField()),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=255)),
                ('lido', models.IntegerField()),
                ('emissorid', models.IntegerField(blank=True, null=True)),
                ('recetorid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'informacaomensagem',
            },
        ),
        migrations.CreateModel(
            name='Informacaonotificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('pendente', models.IntegerField()),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=255)),
                ('lido', models.IntegerField()),
                ('emissorid', models.IntegerField(blank=True, null=True)),
                ('recetorid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'informacaonotificacao',
            },
        ),
        migrations.CreateModel(
            name='Mensagemenviada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem_id', models.IntegerField()),
            ],
            options={
                'db_table': 'mensagemenviada',
            },
        ),
        migrations.CreateModel(
            name='Mensagemrecebida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensagem_id', models.IntegerField()),
            ],
            options={
                'db_table': 'mensagemrecebida',
            },
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=20)),
                ('unread', models.IntegerField()),
                ('actor_object_id', models.CharField(max_length=255)),
                ('verb', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('target_object_id', models.CharField(blank=True, max_length=255, null=True)),
                ('action_object_object_id', models.CharField(blank=True, max_length=255, null=True)),
                ('timestamp', models.DateTimeField()),
                ('public', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('emailed', models.IntegerField()),
                ('data', models.TextField(blank=True, null=True)),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=255)),
                ('action_object_content_type_id', models.IntegerField(blank=True, null=True)),
                ('actor_content_type_id', models.IntegerField()),
                ('recipient_id', models.IntegerField()),
                ('target_content_type_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'notificacao',
            },
        ),
        migrations.CreateModel(
            name='Resgistration',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('date', models.IntegerField(blank=True, db_column='Date', null=True)),
                ('waspresent', models.IntegerField(blank=True, db_column='WasPresent', null=True)),
                ('eventid_event', models.ForeignKey(db_column='EventID_Event', on_delete=django.db.models.deletion.DO_NOTHING, to='Models.event')),
                ('participantuserid', models.ForeignKey(db_column='ParticipantUserID', on_delete=django.db.models.deletion.DO_NOTHING, to='Sessions.participante')),
            ],
            options={
                'db_table': 'resgistration',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='eventtypeid',
            field=models.ForeignKey(db_column='EventTypeID', on_delete=django.db.models.deletion.DO_NOTHING, to='Models.eventtype'),
        ),
        migrations.AddField(
            model_name='event',
            name='formfeedbackid',
            field=models.ForeignKey(db_column='FormFeedBackID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='Event2feedbackForm', to='FormManagement.form'),
        ),
        migrations.AddField(
            model_name='event',
            name='formresgistrationid',
            field=models.ForeignKey(db_column='FormResgistrationID', on_delete=django.db.models.deletion.DO_NOTHING, related_name='Event2registerForm', to='FormManagement.form'),
        ),
        migrations.AddField(
            model_name='event',
            name='proponentid',
            field=models.ForeignKey(db_column='ProponentID', on_delete=django.db.models.deletion.DO_NOTHING, to='Sessions.utilizador'),
        ),
        migrations.CreateModel(
            name='AssetLogistics',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('seats', models.IntegerField(blank=True, db_column='Seats', null=True)),
                ('seatsforreducedmobility', models.IntegerField(blank=True, db_column='SeatsForReducedMobility', null=True)),
                ('quantity', models.IntegerField(db_column='Quantity')),
                ('equipmenttypeid_equipmenttype', models.ForeignKey(blank=True, db_column='EquipmentTypeID_EquipmentType', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.equipmenttype')),
                ('eventid_event', models.ForeignKey(db_column='EventID_Event', on_delete=django.db.models.deletion.DO_NOTHING, to='Models.event')),
                ('servicetypeid_servicetype', models.ForeignKey(blank=True, db_column='ServiceTypeID_ServiceType', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.servicetype')),
            ],
            options={
                'db_table': 'asset_logistics',
            },
        ),
        migrations.CreateModel(
            name='AssetEvent',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('assetid_asset', models.ForeignKey(db_column='AssetID_Asset', on_delete=django.db.models.deletion.DO_NOTHING, to='AssetManagement.asset')),
                ('eventid_event', models.ForeignKey(db_column='EventID_Event', on_delete=django.db.models.deletion.DO_NOTHING, to='Models.event')),
            ],
            options={
                'db_table': 'asset_event',
            },
        ),
    ]
