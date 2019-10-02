from django.urls import path
from .views import *

urlpatterns = [
    path('api/FileUpload', FileUploadView.as_view()),

]