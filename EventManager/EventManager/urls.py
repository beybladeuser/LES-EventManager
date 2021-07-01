"""EventManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
import notifications.urls

urlpatterns = [
    path('forms/', include('FormManagement.urls')),
    path('preEvent/', include('PreEventManagement.urls')),
    path('event/', include('EventManagement.urls')),
    path('asset/', include('AssetManagement.urls')),
    path('utilizadores/', include('utilizadores.urls')),
    path('notificacoes/', include('notificacoes.urls')),
    path('schedules/', include('Schedules.urls')),
    path('', include('Index.urls')),
    path('admin/', admin.site.urls),


    # path('', include("notifications.urls", namespace='notifications')),

  
]
