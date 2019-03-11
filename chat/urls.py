from django.urls import path

from . import views

urlpatterns = [
    path('', views.apartments, name="apartments")
]
