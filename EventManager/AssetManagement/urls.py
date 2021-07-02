from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='assetHome'),
    path('ViewAssets/', views.consultar_assets, name='ViewAssets'),
    path('ViewServices/<int:isPreEdit>/', views.consultar_services, name='ViewServices'),
    path('ViewEquipments/<int:isPreEdit>/', views.consultar_equipments, name='ViewEquiments'),
    path('ViewRooms/<int:isPreEdit>/', views.consultar_rooms, name='ViewRooms'),
    

    path('InsertAsset/', views.createAsset, name='InsertAsset'),
    path('InsertService/', views.createService, name='InsertService'),
    path('InsertEquipment/', views.createEquipment, name='InsertEquipment'),
    path('InsertRoom/', views.createRoom, name='InsertRoom'),

    path('PreDeleteAssets/<int:assetID>/', views.pre_delete_assets, name='PreDeleteAssets'),
    path('DeleteAssets/<int:assetID>/', views.delete_assets, name='DeleteAssets'),



    path('pre_EditService/<int:isPreEdit>/', views.consultar_services, name='pre_EditService'),
    path('pre_EditEquipment/<int:isPreEdit>/', views.consultar_equipments, name='pre_EditEquipment'),
    path('pre_EditRoom/<int:isPreEdit>/', views.consultar_rooms, name='pre_EditRoom'),


    path('EditAsset/<int:assetID>/', views.edit_assets, name='EditAsset'),
    path('EditService/<int:assetID>/', views.createService, name='EditService'),
    path('EditEquipment/<int:assetID>/', views.createEquipment, name='EditEquipment'),
    path('EditRoom/<int:assetID>/', views.createRoom, name='EditRoom'),

    path('PreAssociateAsset/', views.pre_associate_asset, name='PreAssociateAsset'),
    path('AssociateAsset/<int:eventID>/', views.associate_asset, name='AssociateAsset'),
    path('ViewAssociateAssetOfEvent/<int:eventID>/', views.consultar_recursos_disp, name='ViewAssociateAssetOfEvent'),


]