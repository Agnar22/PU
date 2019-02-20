from django.urls import path

from . import views

urlpatterns = [
    path('apartments/<str:location>', views.apartments, name="apartments"),
    path('<int:apartment_id>', views.apartment_detail, name="apartment-detail")
]
