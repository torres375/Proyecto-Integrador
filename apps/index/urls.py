from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from apps.users.views import LoginView



app_name = 'index'

urlpatterns = [
    path('', login_required(views.Login.as_view()), name='index'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('accounts/login/', LoginView.as_view(),name='login'),   
    path('aircraft/create/', views.CreateAircraft.as_view(), name='create_aircraft'),
    path('aircraft/detail/<int:pk>/', views.DetailAircraft.as_view(), name= 'detail_aircraft'),
    path('crew/detail/<int:pk>/', views.DetailCrew.as_view(), name='detail_crew'),
    path('aircraft/list/', views.ListAircraft.as_view(), name='list_aircraft'),
    path('ajax/get_municipalities/', views.get_municipalities, name='ajax_municipalities'),
    path('crew_example/',views.CrewView.as_view(), name='crew_example'),
    path('aircraft/update/<int:pk>/', views.UpdateAircraft.as_view(), name='update_aircraft'),
    path('aircraft/delete/<int:pk>/', views.DeleteAircraft.as_view(), name='delete_aircraft'),
    path('crew_form/',views.CreateCrew.as_view(), name='crew_form'),
    path('crew/list/',views.CrewList.as_view(), name='crew_list'),
    path('crew/update/<int:pk>/', views.UpdateCrew.as_view(), name='update_crew'),
    path('crew/delete/<int:pk>/', views.DeleteCrew.as_view(), name='delete_crew'),
]
