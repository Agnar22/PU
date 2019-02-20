from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from apartments.forms import CreateApartmentForm
from authentication.models import Profile
from .models import Apartment


def apartments(request):
    apartments = Apartment.objects.all()

    context = {
        'apartments': apartments
    }
    return render(request, 'apartments/apartments.html', context)


def apartment_detail(request, apartment_id):
    context = {'id': apartment_id}
    return render(request, 'apartments/apartment-detail.html', context)


def create_apartment(request):
    if request.method == 'GET':
        form = CreateApartmentForm()
        return render(request, 'apartments/create-apartment.html', {'form': form})
    elif request.method == 'POST':
        form = CreateApartmentForm(request.POST, request.FILES or None)
        print(form.errors)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.owner = Profile.objects.get(pk=request.user.pk)
            apartment.image1 = request.FILES['image1']
            print(apartment.image1)
            apartment.save()
            return redirect('profile')
        else:
            print('failed')
            return render(request, 'apartments/create-apartment.html', {'form': form})
