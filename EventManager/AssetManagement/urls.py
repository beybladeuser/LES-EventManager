from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='assetHome'),
    path('ViewAssets/', views.consultar_assets, name='ViewAssets'),
    path('ViewServices/', views.consultar_services, name='ViewServices'),
    path('ViewEquipments/', views.consultar_equipments, name='ViewEquiments'),
    path('ViewRooms/', views.consultar_rooms, name='ViewRooms'),
    
    path('InsertService/', views.createService, name='InsertService'),
    path('InsertEquipment/', views.createEquipment, name='InsertEquipment'),
    path('InsertRoom/', views.createRoom, name='InsertRoom'),

    path('PreDeleteAssets/<int:assetID>/', views.pre_delete_assets, name='PreDeleteAssets'),
    path('DeleteAssets/<int:assetID>/', views.delete_assets, name='DeleteAssets'),

]