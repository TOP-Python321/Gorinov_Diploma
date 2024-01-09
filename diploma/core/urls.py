"""
URL configuration for diploma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# добавлено для работы с медиафайлами
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from smart_house import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('devices/', views.devices,),
    path('devices/', views.DeviceListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DeviceDetailView.as_view(), name='device'),
    path('scenarios/', views.ScenarioListView.as_view(), name='scenarios'),
    path('devices/bat', views.socket_220,name='socket_220'),
    path('wate_pump_form/', views.wate_pump_form, name='wate_pump_form'),
    path('get_data/', views.to_get_data, name='get_data'),
    
]

# для работы с медиафайлами локально
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
