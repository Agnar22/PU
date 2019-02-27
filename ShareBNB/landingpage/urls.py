from django.urls import path

from . import views

urlpatterns = [
    path('', views.landing_page, name="landing-page"),
    path('#login', views.landing_page, name="login"),
    path('#register', views.landing_page, name="register")
]
