from django.urls import path
from .views import *


urlpatterns = [
    path('api/FileUpload', FileUploadView.as_view()),
    path('result/<slug:hashValue>_<int:idValue>', FileResultView),
    path('api/FileUploadAndResult', FileUploadAndResultView.as_view()),
]