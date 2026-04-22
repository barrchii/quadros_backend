from django.urls import path 
from . import views

urlpatterns = [
    path('add/', views.add_to_cart),
    path('', views.get_cart),
    path('remove/<int:item_id>/', views.remove_from_cart),
]