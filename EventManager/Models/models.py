# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection
from FormManagement.models import *
from AssetManagement.models import *
from Sessions.models import *





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



