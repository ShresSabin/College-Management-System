from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
]
