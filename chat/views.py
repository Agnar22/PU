from django.shortcuts import render
from django.shortcuts import render, redirect
from authentication.models import Profile
from .models import Message
from .models import Chat
from django.db.models import Q
import time
import datetime
from django.contrib import messages
from django.http import JsonResponse


def render_chats(request, chat_person=None):
    # Get all chats where the user is
    # Sort after last message recieved
    user_chats = Chat.objects.filter(Q(person1=request.user) | Q(person2=request.user)).order_by('-last_message')

    persons = []  # Persons the user is chatting with
    one_message = []  # The last message in each chat
    for x in range(0, len(user_chats)):
        if user_chats[x].person1 == request.user:
            persons.append(user_chats[x].person2)
        else:
            persons.append(user_chats[x].person1)

        if len(user_chats[x].messages.all()) > 0:
            one_message.append(user_chats[x].messages.all().order_by('-time')[0])
        else:
            one_message.append("")

    # Find current displayed chat
    if chat_person is not None:
        message_chat = get_chat(request.user, chat_person)[0].messages.order_by('time')
    # Display messages from last written chat
    else:
        if len(user_chats) > 0:
            message_chat = user_chats[0].messages.order_by('time')
        else:
            message_chat = ""
        chat_person = persons[0] if len(persons) > 0 else ""
    context = {
        'info': [(one_message[i], persons[i]) for i in range(len(one_message))],
        'messages': message_chat,
        'message_ids':[message.pk for message in message_chat],
        'chatting_with': chat_person
    }
    if request.GET.get('from_vue'):
        return JsonResponse({'last_message': [message.content if not message == "" else "" for message in one_message],
                             'persons': [person.pk for person in persons],
                             'chatting_with': chat_person.pk,
                             'messages': [message.content if not message == "" else "" for message in message_chat],
                             'message_ids': [message.pk for message in message_chat],
                             'message_time':[message.time for message in message_chat]})

    return render(request, 'chat/messages.html', context)


# Returning list of a chats between the two people
def get_chat(person1, person2):
    chat_one = Chat.objects.filter(Q(person1=person1) & Q(person2=person2))
    chat_two = Chat.objects.filter(Q(person1=person2) & Q(person2=person1))
    return chat_one if len(chat_one) > 0 else chat_two


# Send message
def send_message(request):
    message_content = request.POST.get('message', '')
    receiver = request.POST.get('receiver', '')
    curr_message = Message.objects.create(content=message_content, messager=request.user,
                                          reciever=Profile.objects.get(id=receiver),
                                          time=datetime.datetime.now())
    # Finding the correct chat combination
    chat = get_chat(request.user, receiver)
    if len(chat) > 0:
        chat[0].messages.add(curr_message)


# Adding a new chat
def add_chat(request):
    name = request.POST.get('person', '').split()
    if len(name) == 2:
        try:
            chatting_with = Profile.objects.get(first_name=name[0], last_name=name[1])
            Chat.objects.create(person1=request.user, person2=chatting_with)
        except Exception as e:
            messages.error(request, 'Fant dessverre ikke brukeren, prøv på nytt')
            print("Could not add chat\n", e)


# Changing to chat with chat_person_id
def change_chat(request, chat_person_id):
    # Use must be authenticated
    if not request.user.is_authenticated:
        return redirect('landing-page')

    # Add new chat or send message or display other chat
    if request.method == 'POST':
        if request.POST.get('Send', '') == 'Send':
            send_message(request)

        # Add new chat
        elif request.POST.get('Add', '') == 'Add':
            add_chat(request)

    try:
        chatting_with = Profile.objects.get(id=chat_person_id)
    except Exception as e:
        print(e)
        chatting_with = None
    return render_chats(request, chat_person=chatting_with)


# Create your views here.
def chats(request):
    last_chats = Chat.objects.filter(Q(person1=request.user) | Q(person2=request.user)).order_by('-last_message')
    chat_person = None
    if len(last_chats) > 0:
        chat_person = last_chats[0].person1 if request.user is not last_chats[0].person1 else last_chats[0].person2
    return change_chat(request, chat_person)
