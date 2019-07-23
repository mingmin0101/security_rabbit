from django.urls import path
from . import views

urlpatterns = [
    path('api/computerList/',
    views.computerListCreate.as_view()),
    path('api/scanningHistory',views.scanningHistoryListCreate.as_view())
]