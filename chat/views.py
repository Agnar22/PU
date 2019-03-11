from django.shortcuts import render
from django.shortcuts import render, redirect
from authentication.models import Profile
from .models import Message
from .models import Chat
from django.db.models import Q
import time
import datetime

# Create your views here.
def messages(request):
    if not request.user.is_authenticated:
        return redirect('landing-page')

    # Add new chat or send message or display other chat
    if request.method == 'POST':
        message_content = request.POST.get('message', '')
        receiver = request.POST.get('receiver', '')
        curr_message = Message.objects.create(content=message_content, messager=request.user, reciever=Profile.objects.get(id=receiver),
                                              time=datetime.datetime.now())
        print(Profile.objects.get(id=receiver))
        print(Chat.objects.filter(Q(person1=Profile.objects.get(id=receiver))))
        print(Chat.objects.filter(Q(person2=Profile.objects.get(id=receiver))))
        print(Chat.objects.filter(Q(person2=request.user)))
        print(Chat.objects.filter(Q(person1=request.user)))
        print(Chat.objects.filter(Q(person1=Profile.objects.get(id=receiver)) & Q(person2=request.user)))
        print(Chat.objects.filter(Q(person2=Profile.objects.get(id=receiver)) & Q(person1=request.user)))

        chat_one = Chat.objects.filter(Q(person1=request.user) & Q(person2=receiver))
        chat_two = Chat.objects.filter(Q(person1=receiver) & Q(person2=request.user))
        if len(chat_one) > 0:
            chat_one[0].messages.add(curr_message)
        elif len(chat_two):
            chat_two[0].messages.add(curr_message)

    # Display all the chats and
    # Get all chats where this person is
    # Sort after last message recieved
    chats = Chat.objects.filter(Q(person1=request.user) | Q(person2=request.user)).order_by('-last_message')

    persons = []  # Persons the user is chatting with
    one_message = []  # The last message in each chat
    for x in range(0, len(chats)):
        if chats[x].person1 == request.user:
            persons.append(chats[x].person2)
        else:
            persons.append(chats[x].person1)

        if len(chats[x].messages.all()) > 0:
            one_message.append(chats[x].messages.all().order_by('-time')[0])
        else:
            one_message.append()
    # Display messages from last chat
    if len(chats) > 0:
        message_chat = chats[0].messages.order_by('-time')
    else:
        message_chat = ""
    context = {
        'info': [(one_message[i], persons[i]) for i in range(len(one_message))],
        'messages': message_chat,
        'chatting_with': persons[0]
    }
    return render(request, 'chat/messages.html', context)
