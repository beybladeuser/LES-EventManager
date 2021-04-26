from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Administrador(models.Model):
    utilizador_ptr_id = models.IntegerField(primary_key=True)
    gabinete = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'administrador'


class Colaborador(models.Model):
    utilizador_ptr_id = models.IntegerField(primary_key=True)
    curso_id = models.IntegerField()
    departamento_id = models.IntegerField()
    faculdade_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'colaborador'


class Coordenador(models.Model):
    utilizador_ptr_id = models.IntegerField(primary_key=True)
    gabinete = models.CharField(db_column='Gabinete', max_length=255)  # Field name made lowercase.
    departamentoid = models.IntegerField(db_column='DepartamentoID')  # Field name made lowercase.
    faculdadeid = models.IntegerField(db_column='FaculdadeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'coordenador'


class Participante(models.Model):
    utilizador_ptr_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'participante'


class Professoruniversitario(models.Model):
    utilizador_ptr_id = models.IntegerField(primary_key=True)
    gabinete = models.CharField(db_column='Gabinete', max_length=255)  # Field name made lowercase.
    departamento_id = models.IntegerField()
    faculdade_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'professoruniversitario'

class Responsavel(models.Model):
    nome = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    tel = models.CharField(max_length=128)
    inscricao_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'responsavel'


class Utilizador(models.Model):
    user_ptr_id = models.IntegerField(primary_key=True)
    contacto = models.CharField(max_length=20)
    valido = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'utilizador'