from django.contrib import admin
from .models import *

# Register your models here.


admin.register(medtrac_log)(admin.ModelAdmin)
admin.register(food_log)(admin.ModelAdmin)
admin.register(config_discomfort)(admin.ModelAdmin)
admin.register(HealthIncidentLogs)(admin.ModelAdmin)
