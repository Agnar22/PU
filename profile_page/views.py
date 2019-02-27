from django.shortcuts import render, redirect
from django.contrib.auth import logout

from apartments.models import Apartment
from authentication.forms import RegisterForm
from authentication.models import Profile


def logout_view(request):
    logout(request)
    return redirect('landing-page')


def delete_user(request):
    if request.method == 'POST' and request.user.is_authenticated:
        user = Profile.objects.get(pk=request.user.pk)
        user.delete()
        return redirect('landing-page')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        user = Profile.objects.get(pk=request.user.pk)
        form = RegisterForm(instance=user)
        context = {
            'my_apartments': Apartment.objects.filter(owner=request.user),
            'form': form
        }
        if request.method == 'GET':
            return render(request, 'profile_page/profile-page.html', context)
        else:  # POST
            form = RegisterForm(request.POST, instance=user)
            print(form.errors)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.phone_number = form.cleaned_data['phone_number']
            user.save()
            return render(request, 'profile_page/profile-page.html', context)

