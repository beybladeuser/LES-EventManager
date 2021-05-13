from django.contrib import admin
from .models import Utilizador,Administrador,Participante,Proponente
# Register your models here.
admin.site.register(Utilizador)

admin.site.register(Administrador)

admin.site.register(Participante)

admin.site.register(Proponente)
