from django.urls import path, include
from MEDTRAC import views

urlpatterns = [
    path('', views.medtrac_dashboard, name='Medtrac_home'),
    path('log_medtrac/', views.log_medtrac),
    path('get_data_by_id', views.get_data_by_id),
    path('update_data_by_id', views.update_data_by_id),
    path('delete_data_by_id', views.delete_data_by_id),
    path('add_health_incident', views.add_health_incident),
    path('food_log/', views.food_logger),
    path('food_tracker/', views.food_tracker_home),
    path('log_food_data', views.log_food_data),
    path('graph_data', views.food_tracker_graph_data),
    path('delete_foodlog', views.delete_foodlog),
    path('edit_foodlog', views.edit_foodlog),

]
