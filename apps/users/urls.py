from django.contrib import admin 
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import *

app_name = 'users'
urlpatterns = [  
    # Enter the app name in following syntax for this to work 
    path('register_user/', UserRegister.as_view(), name="register"),
    path('detail/<int:pk>/', UserDetail.as_view(), name="detail"),
    path('update/<int:pk>/', UserUpdate.as_view(), name="update"), 
    path('delete/<int:pk>/', UserDelete.as_view(), name="delete"),
    path('disable_enable/<int:pk>/', UserDisable.as_view(), name="disable_enable"),
    path('list/', UserList.as_view(), name="list"),
    path('change_password/', ChangeMyPasswordUpdate.as_view(), name="change_password"),
]