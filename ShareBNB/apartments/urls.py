from django.urls import path

from . import views

urlpatterns = [
    path('', views.apartments, name="apartments"),
    path('<int:apartment_id>', views.apartment_detail, name="apartment-detail"),
    path('create', views.create_apartment, name="create-apartment")
]
