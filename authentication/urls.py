from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('login/', views.LoginFormView, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterFormView, name='register'),
]
