from django.urls import path
from . import views

urlpatterns = [
    path('api/User', views.UserView),
    path('generate/User', views.GenerateRandomUserView.as_view(), name='generate'),
    path('', views.UsersListView.as_view(), name='users_list'),
]