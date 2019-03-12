from django.urls import path

from . import views

urlpatterns = [
    path('', views.chats, name="chat"),
    path('<slug:chat_person_id>', views.change_chat, name="chat")
]
