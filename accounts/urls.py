from django.urls import path
from . import views

urlpatterns = [
    path('send-code/', views.send_code),
    path('verify-code/', views.verify_code),
    path('check/', views.check_auth),
    path('logout/', views.logout_view),
    path('delete/', views.delete_account),
]

