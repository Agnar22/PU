from django.urls import path

from . import views

urlpatterns = [
    path('profile', views.profile_view, name="profile"),
    path('delete-user', views.delete_user, name="delete-user"),
]
