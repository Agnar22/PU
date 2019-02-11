from django.urls import path

from . import views

urlpatterns = [
    path('', views.apartments, name="apartments"),
    # path('<id:apartment_id>', views.apartment_detail, name="apartment-detail")
]
