from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='assetHome'),
    path('ViewAssets', views.consultar_assets, name='ViewAssets'),
    path('ViewServices', views.consultar_services, name='ViewServices'),
    path('ViewEquipments', views.consultar_equipments, name='ViewEquiments'),
    path('ViewRooms', views.consultar_rooms, name='ViewRooms'),
    path('InsertAssets', views.insert_assets, name='InsertAssets'),
        

]