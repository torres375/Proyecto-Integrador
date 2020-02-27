from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from apps.users.views import LoginView


app_name = 'index'

urlpatterns = [
    path('', login_required(views.Login.as_view()), name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('accounts/login/', LoginView.as_view(),name='login'),
    path('table_example', views.TableExample.as_view(), name='table_example'),
    path('form_example', views.FormExample.as_view(), name='form_example'),
]