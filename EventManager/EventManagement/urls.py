from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewanswer, name='eventHome'),
    path('cancelregistration/<int:RegistrationID>', views.cancelregistration, name='cancelregistration'),
    #path('checkboxvalues/<int:waspresent>', views.checkboxvalues, name='checkboxvalues'),
    path('consultar_participantes/<int:eventid_event>', views.consultar_participantes, name='consultar_participantes'),
    path('addregistration/<int:EventID>', views.addregistration, name='addregistration'),
    path('consultar_participantes/Anwsers/<int:RegistrationID>', views.viewanswer, name='viewanswer'),
]