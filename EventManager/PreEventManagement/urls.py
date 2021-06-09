from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='preEventHome'),

    path('list', views.list, name='list'),
    path('list/<str:sort_key>', views.list, name='list_sort'), 

    path('create', views.create, name='create'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('validate/<int:id>', views.validate, name='validate'),
    path('enroll/<int:id>', views.enroll, name='enroll'),

]