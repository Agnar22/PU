from django.shortcuts import render
from django.shortcuts import render, redirect
from apartments.forms import CreateApartmentForm
from authentication.models import Profile
from .models import Message
from .models import Chat
from django.db.models import Q


# Create your views here.
def messages(request):
    # Display all the chats and
    if request.method('GET'):
        if request.user.is_authenticated:
            # Get all chats where this person is
            # Sort after last message recieved
            chats = Chat.objects.filter(Q(person1=request.user) | Q(person2=request.user)).order_by('-last_message')

            persons = []  # Persons the user is chatting with
            one_message = []  # The last message in each chat
            for x in range(0, len(chats)):
                if chats[x].person1 == request.user:
                    persons.append(chats[x].person1)
                else:
                    persons.append(chats[x].person2)
                one_message.append(chats[x].messages.objects.all().order_by('-time'))

            # Display messages from last chat
            message_chat = chats[0].messages.order_by('-time')
            context = {
                'messages': message_chat,
                'persons': persons,
                'one_message': one_message

            }
            return render(request, 'chat/messages.html', context)
        else:
            return redirect('landing-page')
        pass
    # Add new chat or send message or display other chat
    else:
        pass

    pass
