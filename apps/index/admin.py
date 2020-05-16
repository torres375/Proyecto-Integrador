from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Department)
admin.site.register(Municipality)
admin.site.register(AirCraftType)
admin.site.register(AirCraftModel)
admin.site.register(AirCraft)
admin.site.register(Rank)
admin.site.register(UserType)
admin.site.register(MajorOperativeUnit)
admin.site.register(MinorOperativeUnit)
admin.site.register(TacticUnit)
admin.site.register(UserProfile)
admin.site.register(Crew)   
admin.site.register(MajorOperation)
admin.site.register(Operation)
admin.site.register(FlightCondition)
admin.site.register(AviationEvent)
admin.site.register(MissionType)
admin.site.register(AviationMission)
admin.site.register(Agreement)
admin.site.register(Configuration)
admin.site.register(FlightReport)
admin.site.register(AirCrew)
admin.site.register(AssignedHourMajorOperationAircraftModel)
admin.site.register(AssignedHourAgreementAircraftModel)