from django.contrib import admin

from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('content', 'messager', 'reciever', 'time', 'date')

    class Meta:
        model = Message

class ChatAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('messages', 'person1', 'person2', 'last_message', 'last_message_date')

    class Meta:
        model = Chat


admin.site.register(Message, MessageAdmin)
admin.site.register(Chat, ChatAdmin)