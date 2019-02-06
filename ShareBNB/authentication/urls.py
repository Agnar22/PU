from django.urls import path
from django.contrib.auth import logout

from . import views

urlpatterns = [
    path('logout/', views.logout_user, name='logout'),
]
