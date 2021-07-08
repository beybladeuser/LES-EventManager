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




    path('EditAsset/<int:assetID>/', views.edit_assets, name='EditAsset'),
    path('EditService/<int:assetID>/', views.createService, name='EditService'),
    path('EditEquipment/<int:assetID>/', views.createEquipment, name='EditEquipment'),
    path('EditRoom/<int:assetID>/', views.createRoom, name='EditRoom'),

    path('ViewAssociateAsset/', views.view_associate_asset, name='ViewAssociateAsset'),
    
    path('ViewAssetsToAssociate/<int:eventID>/', views.consultar_recursos_para_add, name='ViewAssetsToAssociate'),
    
    path('AssociateAsset/<int:eventID>/<int:assetID>/', views.associate_asset, name='AssociateAsset'),
    path('AssociateAssetV2/<int:assocID>/', views.associate_assetV2, name='AssociateAssetV2'),

    path('ViewAssetsOfEvent/<int:eventID>/', views.consultar_recursos_do_evento, name='ViewAssetsOfEvent'),

    path('DeassociateAssetsOfEvent/<int:eventID>/<int:assetID>/', views.desassociar_recurso, name='DeassociateAssetsOfEvent'),
    path('Detalhes/<int:assetID>/', views.detalhes, name='Detalhes'),
    
]