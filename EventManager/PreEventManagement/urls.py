from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='preEventHome'),
    path('list', views.list, name='list'),
    path('create', views.create, name='create'),
    path('edit/<int:id>', views.list, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('validate/<int:id>', views.validate, name='validate')
]