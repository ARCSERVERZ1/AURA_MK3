
from django.urls import path , include
from AIGIC import views as aigic



urlpatterns = [
    path('load_vector_db' , aigic.load_vector_db),
    path('rag_query' , aigic.rag_query),
    ]