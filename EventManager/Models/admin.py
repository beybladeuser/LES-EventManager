from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AssetEvent)
admin.site.register(AssetLogistics)


admin.site.register(Event)
admin.site.register(Eventtype)
admin.site.register(Informacaomensagem)
admin.site.register(Informacaonotificacao)
admin.site.register(Mensagemenviada)
admin.site.register(Mensagemrecebida)
admin.site.register(Notificacao)
admin.site.register(Resgistration)