from django.urls import path

from . import views

urlpatterns = [
    path('', views.formsHome, name='formsHome'),
    path('listformsfromtype/<int:formTypeID>/', views.listFormsFromType, name='listFormsFromType'),
    path('listformsfromtype/', views.listFormsFromType, name='listFormsFromType'),
    path('checkform/', views.checkForm, name='checkForm'),
    path('checkform/<int:formID>/', views.checkForm, name='checkForm'),
    path('checkformlayout/', views.checkFormLayout, name='checkFormLayout'),
    path('checkformlayout/<int:formID>/', views.checkFormLayout, name='checkFormLayout'),

    path('createform/', views.createForm, name='createForm'),
    path('createform/<int:formTypeID>/', views.createForm, name='createForm'),
    path('createform/<int:formTypeID>/<int:formID>/', views.createForm, name='createForm'),
]