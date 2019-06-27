"""security_rabbit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path ,include,register_converter
from panel.views import userPage, showDetail, showScanningDetail, showFileDetail
from django.urls.converters import SlugConverter,StringConverter

register_converter(StringConverter, 'computerName')
urlpatterns = [
    # path('upload/', )   從殼下載檔案
    path('user/', userPage) ,  #使用者看的頁面
    path('admin/', admin.site.urls),
    path('computer/<str:computerName>/',showDetail),
    path('computer/<str:computerName>/<int:sequence>/',showScanningDetail),
    path('file/<str:computerName>/<str:fileName>/',showFileDetail)
]
