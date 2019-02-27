from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from authentication.forms import RegisterForm, LoginForm
from authentication.models import Profile


def landing_page(request):
    form = RegisterForm()
    if request.method == 'GET':
        context = {
            'form': form
        }
        return render(request, 'landingpage/landing-page.html', context)

    else: #POST
        if request.POST.get("first_name"): #Register
            print("Registrering")
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)

                # Cleaned (normalized) data
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                # Returns User objects if credentials are correct
                user = authenticate(email=email, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)  # User is logged in
                        return redirect('/')

            return render(request, 'landingpage/landing-page.html', {'form': form})
        else:
            print("Login")
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing-page')
            else:
                messages.warning(request, f'Finner ingen bruker med tilsvarende mail og passord!')
                return redirect('landing-page')

