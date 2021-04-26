from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ViewAssets', views.consultar_assets, name='ViewAssets'),
    path('ViewServices', views.consultar_services, name='ViewServices'),
    path('ViewEquipments', views.consultar_equipments, name='ViewEquiments'),
    path('ViewRooms', views.consultar_rooms, name='ViewRooms'),
        

]