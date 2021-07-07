from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='preEventHome'),

    path('list', views.listing, name='list'),
    path('list/<str:sort_key>', views.listing, name='list_sort'), 

    path('create', views.create, name='create'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('validate/<int:id>/<int:validate>', views.validate, name='validate'),
    path('fill_logistic/<int:id>', views.fill_logistic, name='fill_logistic'),
    path('edit_logistic/<int:id>', views.edit_logistic, name='edit_logistic'),
    path('remove_all_assets/<int:id>', views.remove_all_assets, name='remove_all_assets'),
    path('feedback/<int:id>', views.feedback, name='feedback'),

]