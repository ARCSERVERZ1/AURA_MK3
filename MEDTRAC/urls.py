from django.urls import path , include
from MEDTRAC import views
urlpatterns = [
    path('' , views.medtrac_dashboard),
    path('log_medtrac/',views.log_medtrac),
    path('add_health_incident',views.add_health_incident),
    path('food_log/',views.food_logger)
]
