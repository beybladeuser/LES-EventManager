from django.urls import path

from . import views

urlpatterns = [
    path('cancelregistration/<int:RegistrationID>', views.cancelregistration, name='cancelregistration'),
]