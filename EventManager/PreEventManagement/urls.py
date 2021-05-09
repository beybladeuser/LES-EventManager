from django.urls import path

from . import views

urlpatterns = [
    path('', views.preEventHome, name='preEventHome'),
    path('', views.preEvent, name='preEvent')
]