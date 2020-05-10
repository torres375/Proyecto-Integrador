from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views, utils, utilspdf
from apps.users.views import LoginView, logout_view
from apps.index.views import *



app_name = 'index'

urlpatterns = [
    # path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('', LoginView.as_view(),name='login'),
    path('logout/', logout_view,name='logout'),   
    
    path('aircraft/list/', views.ListAircraft.as_view(), name='list_aircraft'),
    path('aircraft/create/', views.CreateAircraft.as_view(), name='create_aircraft'),
    path('aircraft/detail/<int:pk>/', views.DetailAircraft.as_view(), name= 'detail_aircraft'),
    path('aircraft/update/<int:pk>/', views.UpdateAircraft.as_view(), name='update_aircraft'),
    path('aircraft/delete/<int:pk>/', views.DeleteAircraft.as_view(), name='delete_aircraft'),
    path('ajax/get_municipalities/', views.get_municipalities, name='ajax_municipalities'),
    path('ajax/get_aircraft_models/', views.get_aircraft_models, name='ajax_aircraft_models'),
    path('ajax/get_aircrafts/', views.get_aircrafts, name='ajax_aircrafts'),
    path('ajax/get_aviation_missions/', views.get_aviation_missions, name='ajax_aviation_missions'),
    path('ajax/get_operations/', views.get_operations, name='ajax_operations'),

    # path('crew_example/',views.CrewView.as_view(), name='crew_example'),
    path('crew/list/',views.ListCrew.as_view(), name='list_crew'),
    path('crew/create/',views.CreateCrew.as_view(), name='create_crew'),
    path('crew/detail/<int:pk>/', views.DetailCrew.as_view(), name='detail_crew'),
    path('crew/update/<int:pk>/', views.UpdateCrew.as_view(), name='update_crew'),
    path('crew/delete/<int:pk>/', views.DeleteCrew.as_view(), name='delete_crew'),

    path('uoma/list/', views.ListUOMA.as_view(), name='list_uoma'),
    path('uoma/create/', views.CreateUOMA.as_view(), name='create_uoma'),
    path('uoma/detail/<int:pk>/', views.DetailUOMA.as_view(), name= 'detail_uoma'),
    path('uoma/update/<int:pk>/', views.UpdateUOMA.as_view(), name='update_uoma'),
    path('uoma/delete/<int:pk>/', views.DeleteUOMA.as_view(), name='delete_uoma'),

    path('uome/list/', views.ListUOME.as_view(), name='list_uome'),
    path('uome/create/', views.CreateUOME.as_view(), name='create_uome'),
    path('uome/detail/<int:pk>/', views.DetailUOME.as_view(), name= 'detail_uome'),
    path('uome/update/<int:pk>/', views.UpdateUOME.as_view(), name='update_uome'),
    path('uome/delete/<int:pk>/', views.DeleteUOME.as_view(), name='delete_uome'),

    path('tactic_unit/list/', views.ListTacticUnit.as_view(), name='list_tactic_unit'),
    path('tactic_unit/create/', views.CreateTacticUnit.as_view(), name='create_tactic_unit'),
    path('tactic_unit/detail/<int:pk>/', views.DetailTacticUnit.as_view(), name= 'detail_tactic_unit'),
    path('tactic_unit/update/<int:pk>/', views.UpdateTacticUnit.as_view(), name='update_tactic_unit'),
    path('tactic_unit/delete/<int:pk>/', views.DeleteTacticUnit.as_view(), name='delete_tactic_unit'),

    path('major_operation/list/', views.ListMajorOperation.as_view(), name='list_major_operation'),
    path('major_operation/create/', views.CreateMajorOperation.as_view(), name='create_major_operation'),
    path('major_operation/detail/<int:pk>/', views.DetailMajorOperation.as_view(), name= 'detail_major_operation'),
    path('major_operation/update/<int:pk>/', views.UpdateMajorOperation.as_view(), name='update_major_operation'),
    path('major_operation/delete/<int:pk>/', views.DeleteMajorOperation.as_view(), name='delete_major_operation'),

    path('operation/list/', views.ListOperation.as_view(), name='list_operation'),
    path('operation/create/', views.CreateOperation.as_view(), name='create_operation'),
    path('operation/detail/<int:pk>/', views.DetailOperation.as_view(), name= 'detail_operation'),
    path('operation/update/<int:pk>/', views.UpdateOperation.as_view(), name='update_operation'),
    path('operation/delete/<int:pk>/', views.DeleteOperation.as_view(), name='delete_operation'),

    path('flight_condition/list/', views.ListFlightCondition.as_view(), name='list_flight_condition'),
    path('flight_condition/create/', views.CreateFlightCondition.as_view(), name='create_flight_condition'),
    path('flight_condition/detail/<int:pk>/', views.DetailFlightCondition.as_view(), name= 'detail_flight_condition'),
    path('flight_condition/update/<int:pk>/', views.UpdateFlightCondition.as_view(), name='update_flight_condition'),
    path('flight_condition/delete/<int:pk>/', views.DeleteFlightCondition.as_view(), name='delete_flight_condition'),

    path('agreement/list/', views.ListAgreement.as_view(), name='list_agreement'),
    path('agreement/create/', views.CreateAgreement.as_view(), name='create_agreement'),
    path('agreement/detail/<int:pk>/', views.DetailAgreement.as_view(), name= 'detail_agreement'),
    path('agreement/update/<int:pk>/', views.UpdateAgreement.as_view(), name='update_agreement'),
    path('agreement/delete/<int:pk>/', views.DeleteAgreement.as_view(), name='delete_agreement'),

    path('aircraft_type/list/', views.ListAirCraftType.as_view(), name='list_aircraft_type'),
    path('aircraft_type/create/', views.CreateAirCraftType.as_view(), name='create_aircraft_type'),
    path('aircraft_type/detail/<int:pk>/', views.DetailAirCraftType.as_view(), name= 'detail_aircraft_type'),
    path('aircraft_type/update/<int:pk>/', views.UpdateAirCraftType.as_view(), name='update_aircraft_type'),
    path('aircraft_type/delete/<int:pk>/', views.DeleteAirCraftType.as_view(), name='delete_aircraft_type'),

    path('aircraft_model/list/', views.ListAirCraftModel.as_view(), name='list_aircraft_model'),
    path('aircraft_model/create/', views.CreateAirCraftModel.as_view(), name='create_aircraft_model'),
    path('aircraft_model/detail/<int:pk>/', views.DetailAirCraftModel.as_view(), name= 'detail_aircraft_model'),
    path('aircraft_model/update/<int:pk>/', views.UpdateAirCraftModel.as_view(), name='update_aircraft_model'),
    path('aircraft_model/delete/<int:pk>/', views.DeleteAirCraftModel.as_view(), name='delete_aircraft_model'),

    path('aviation_event/list/', views.ListAviationEvent.as_view(), name='list_aviation_event'),
    path('aviation_event/create/', views.CreateAviationEvent.as_view(), name='create_aviation_event'),
    path('aviation_event/detail/<int:pk>/', views.DetailAviationEvent.as_view(), name= 'detail_aviation_event'),
    path('aviation_event/update/<int:pk>/', views.UpdateAviationEvent.as_view(), name='update_aviation_event'),
    path('aviation_event/delete/<int:pk>/', views.DeleteAviationEvent.as_view(), name='delete_aviation_event'),

    path('mission_type/list/', views.ListMissionType.as_view(), name='list_mission_type'),
    path('mission_type/create/', views.CreateMissionType.as_view(), name='create_mission_type'),
    path('mission_type/detail/<int:pk>/', views.DetailMissionType.as_view(), name= 'detail_mission_type'),
    path('mission_type/update/<int:pk>/', views.UpdateMissionType.as_view(), name='update_mission_type'),
    path('mission_type/delete/<int:pk>/', views.DeleteMissionType.as_view(), name='delete_mission_type'),

    path('aviation_mission/list/', views.ListAviationMission.as_view(), name='list_aviation_mission'),
    path('aviation_mission/create/', views.CreateAviationMission.as_view(), name='create_aviation_mission'),
    path('aviation_mission/detail/<int:pk>/', views.DetailAviationMission.as_view(), name= 'detail_aviation_mission'),
    path('aviation_mission/update/<int:pk>/', views.UpdateAviationMission.as_view(), name='update_aviation_mission'),
    path('aviation_mission/delete/<int:pk>/', views.DeleteAviationMission.as_view(), name='delete_aviation_mission'),

    path('configuration/list/', views.ListConfiguration.as_view(), name='list_configuration'),
    path('configuration/create/', views.CreateConfiguration.as_view(), name='create_configuration'),
    path('configuration/detail/<int:pk>/', views.DetailConfiguration.as_view(), name= 'detail_configuration'),
    path('configuration/update/<int:pk>/', views.UpdateConfiguration.as_view(), name='update_configuration'),
    path('configuration/delete/<int:pk>/', views.DeleteConfiguration.as_view(), name='delete_configuration'),

    path('flight_report/list/', views.ListFlightReport.as_view(), name='list_flight_report'),
    path('flight_report/detail/<str:pk>/', views.DetailFlightReport.as_view(), name='detail_flight_report'),
    path('flight_report/create/', views.CreateFlightReport.as_view(), name='create_flight_report'),
    path('flight_report/get_crew/', views.CrewFormView.as_view(), name='get_crew'),
    path('ajax/get_minor_operative_units/', views.get_minor_operative_units, name='ajax_minor_operative_units'),
    path('ajax/get_tactic_units/', views.get_tactic_unit, name='ajax_get_tactic_units'),
    path('ajax/get_aviation_tactic_units/', views.get_tactic_unit_aviation, name='ajax_get_aviation_tactic_units'),
    path('flight_report/excel/', utils.ReportAircratfExcel.as_view(), name='report_aircraft_excel'),
    path('flight_report/excel2/', utils.ExcelHoursAircraft.as_view(), name='report_aircraft_excel2'),
    path('flight_report/list/', views.ListPdf.as_view(), name='report_aircraft_pdf'),
    path('flight_report/pdf/', views.gen_pdf,name='pdf'),
# graph
    path('graph/graph_bar/', views.graphic_bar_years,name='graph_bar'),
    path('graph/graph_bar_battalion/', views.graph_bar_battalion,name='graph_bar_battalion'),
    path('graph/graph_bar_aircraft_model_hours/', graph_bar_aircraft_model_hours, name='graph_bar_aircraft_model_hours'),

    path('graph/graphic_pie_operational/', views.graph_pie_operational,name='graphic_pie_operational'),
    path('graph/graphic_pie_no_operational/', views.graphic_pie_no_operational,name='graphic_pie_no_operational'),

]
