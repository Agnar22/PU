from django.urls import path

from . import views

urlpatterns = [
    path('', views.apartments, name="apartments"),
    path('<int:apartment_id>/<slug:start_date>/<slug:end_date>', views.apartment_detail, name="apartment-detail"),
    path('create', views.create_apartment, name="create-apartment"),
    path('edit/<int:apartment_id>', views.edit_apartment, name="edit-apartment")
]
