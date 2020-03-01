from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Department)
admin.site.register(Municipality)
admin.site.register(AirCraftType)
admin.site.register(AirCraftModel)
admin.site.register(Aircraft)

