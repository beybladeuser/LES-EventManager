from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Asset)
admin.site.register(Building)
admin.site.register(Campus)
admin.site.register(Equipment)
admin.site.register(Equipmenttype)
admin.site.register(Rooms)
admin.site.register(Service)
admin.site.register(Servicetype)