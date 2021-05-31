from django.urls import path

from . import views

urlpatterns = [
    path('', views.viewanswer, name='eventHome'),
    path('cancelregistration/<int:RegistrationID>', views.cancelregistration, name='cancelregistration'),
    path('consultar_participantes/<int:eventid_event>', views.consultar_participantes, name='consultar_participantes'),
    path('addregistration/<int:EventID>', views.addregistration, name='addregistration'),
    path('consultar_participantes/Anwsers/<int:RegistrationID>', views.viewanswer, name='viewanswer'),
    path('consultar_participantesnaovalidados/<int:eventid_event>', views.consultar_participantesnaovalidados, name='consultar_participantesnaovalidados'),
    path('chekout/<int:RegistrationID>', views.checkout, name='checkout'),
    path('chekin/<int:RegistrationID>', views.checkin, name='checkin'),
    path('validateparticipant/<int:RegistrationID>', views.validateparticipant, name='validateparticipant'),
    
]