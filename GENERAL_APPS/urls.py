from django.urls import path , include
from GENERAL_APPS import views
urlpatterns = [
    path('location/home',views.form_save_loc, name = 'location_home'),
    path('location/save_loc',views.save_loc),
    path('location/get_data_by_id/',views.get_data_by_id),
    path('location/delete_by_id/',views.delete_by_id),
    path('test/',views.test_run),
    path('home_query/',views.home_query),
    path('checklist/',views.checklist_dashboard),
    path('checklist_data',views.checklist_dashboard_data),
    path('checkpoint_data',views.checkpoint_data),
    path('edited_check_point',views.edited_check_point),


]
