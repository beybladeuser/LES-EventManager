from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Informacaomensagem)
admin.site.register(Informacaonotificacao)
admin.site.register(Mensagemenviada)
admin.site.register(Mensagemrecebida)
admin.site.register(Notificacao)