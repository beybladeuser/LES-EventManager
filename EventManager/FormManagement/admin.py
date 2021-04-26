from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Answer)
admin.site.register(Form)
admin.site.register(Formtype)
admin.site.register(Multipleoptions)
admin.site.register(Questions)
admin.site.register(QuestionsForm)
admin.site.register(Questiontype)