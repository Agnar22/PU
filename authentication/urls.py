from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginFormView, name='login'),
]

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
]

urlpatterns = [
    path('register/', views.RegisterFormView, name='register'),
]