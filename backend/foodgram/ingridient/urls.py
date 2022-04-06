from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingridient_get),
    path('<id>/', views.ingridient_id_get),
]
