from django.urls import path

from . import views

urlpatterns = [
    path('', views.review, name="review"),
    path('<int:tenant_pk>/<int:subtenant_pk>/<int:apartment_pk>/<int:contract_pk>', views.user_and_apartment_review,
         name="review")
]
