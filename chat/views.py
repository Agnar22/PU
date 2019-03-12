from django.shortcuts import render
from django.shortcuts import render, redirect
from authentication.models import Profile
from .models import Message
from .models import Chat
from django.db.models import Q
import time
import datetime
from django.contrib import messages


# Create your views here.
def chats(request, viewing_chat=None):
    if not request.user.is_authenticated:
        return redirect('landing-page')

    # Add new chat or send message or display other chat
    if request.method == 'POST':
        # Send message
        if request.POST.get('Send', '') == 'Send':
            message_content = request.POST.get('message', '')
            receiver = request.POST.get('receiver', '')
            curr_message = Message.objects.create(content=message_content, messager=request.user,
                                                  reciever=Profile.objects.get(id=receiver),
                                                  time=datetime.datetime.now())
            # Finding the correct chat combination
            chat_one = Chat.objects.filter(Q(person1=request.user) & Q(person2=receiver))
            chat_two = Chat.objects.filter(Q(person1=receiver) & Q(person2=request.user))
            if len(chat_one) > 0:
                chat_one[0].messages.add(curr_message)
            elif len(chat_two):
                chat_two[0].messages.add(curr_message)

        # Add new chat
        elif request.POST.get('Add', '') == 'Add':
            name = request.POST.get('person', '').split()
            if len(name) == 2:
                try:
                    chatting_with = Profile.objects.get(first_name=name[0], last_name=name[1])
                    Chat.objects.create(person1=request.user, person2=chatting_with)
                except Exception as e:
                    messages.error(request, 'Fant dessverre ikke brukeren, prøv på nytt')
                    print("Could not add chat\n", e)

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
            one_message.append("")
    # Display messages from last chat
    if len(chats) > 0:
        message_chat = chats[0].messages.order_by('-time')
    else:
        message_chat = ""
    chatting_with = persons[0] if len(persons) > 0 else ""
    context = {
        'info': [(one_message[i], persons[i]) for i in range(len(one_message))],
        'messages': message_chat,
        'chatting_with': chatting_with
    }
    return render(request, 'chat/messages.html', context)
