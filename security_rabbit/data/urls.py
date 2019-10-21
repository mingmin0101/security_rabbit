from django.urls import path
from . import views

urlpatterns = [
    path('api/Computer', views.ComputerView),
    path('api/ScanningRecord', views.ScanningRecordView),
    path('api/ScanningDetails', views.ScanningDetailsView),
    path('api/FileInfo', views.FileInfoView),

    path('download_scanfile', views.download_scanfile),

    path('uploadxml/',views.uploadxml),
    path('downloadzip/<slug:filename>',views.downloadzip),

]