from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.db.models import Count
from apartments.models import Apartment
from authentication.forms import RegisterForm, LoginForm
from authentication.models import Profile
from django.contrib import messages


def landing_page(request):
    form = RegisterForm()

    distinct_cities = Apartment.objects.values('city').distinct().count()
    distinct_apartments = Apartment.objects.all().count()

    if request.method == 'GET':
        context = {
            'form': form,
            'distinct_cities': distinct_cities,
            'distinct_apartments': distinct_apartments
        }
        return render(request, 'landingpage/landing-page.html', context)

    else: #POST
        if request.POST.get("first_name"): #Register
            print("Registrering")
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)

                # Cleaned (normalized) data
                email = form.cleaned_data['email'].lower()
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()

                # Returns User objects if credentials are correct
                user = authenticate(email=email, password=password)

                if user is not None:
                    if user.is_active:
                        login(request, user)  # User is logged in
                        messages.success(request, 'Du er nå registrert og logget inn!')
                        return redirect('/')
            else:
                messages.warning(request, form.errors)
            return render(request, 'landingpage/landing-page.html', {'form': form, 'distinct_cities': distinct_cities,
                                                                    'distinct_apartments': distinct_apartments})
        else:
            email = request.POST.get("email").lower()
            password = request.POST.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Du er nå logget inn!')
                return redirect('landing-page')
            else:
                messages.error(request, 'Fant dessverre ikke brukeren, prøv på nytt')
                return redirect('landing-page')

