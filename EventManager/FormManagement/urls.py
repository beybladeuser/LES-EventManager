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
    path('deleteform/<int:formID>/', views.deleteForm_action, name='deleteForm'),

    path('createquestion/<int:questionID>/<int:formID>/', views.createQuestion, name='createQuestion'),

    path('listquestions/', views.listQuestions, name='listQuestions'),
    path('listquestions/<int:formID>', views.listQuestions, name='listQuestions'),


    path('associatequestion/<int:questionID>/<int:formID>/', views.associateQuestion, name='associateQuestion'),
    path('deassociatequestion/<int:questionID>/<int:formID>/', views.deassociateQuestion, name='deassociateQuestion'),

    path('createoption/<int:questionID>/<int:optionID>/', views.createOption, name='createOption'),
    path('createoption/<int:questionID>/', views.createOption, name='createOption'),
    
    
    path('deleteoption/<int:questionID>/<int:optionID>/', views.deleteOption, name='deleteOption'),

    path('deletequestion/<int:questionID>/', views.deleteQuestion, name='deleteQuestion'),


    path('test/', views.testForm, name='test'),
]