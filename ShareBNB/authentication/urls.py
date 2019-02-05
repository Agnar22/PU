from django.urls import path
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
]
