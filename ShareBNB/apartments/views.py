import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from apartments.forms import CreateApartmentForm
from authentication.models import Profile
from .models import Apartment
from django.db.models import Q


def apartments(request):
    location_query = request.GET.get("location")
    guests_query = request.GET.get("guests")
    start_date_query = request.GET.get("start_date")
    end_date_query = request.GET.get("end_date")




    #---------------------------------------------------
    #Filter basert på lokasjon og antall sengeplasser:


    if(location_query != None and guests_query != None):
        apartments = Apartment.objects.filter((
            Q(city__icontains = location_query) |
            Q(country__icontains = location_query) |
            Q(address__icontains = location_query)) &
            Q(beds__gte = guests_query)).distinct()

    elif(location_query != None and guests_query == None):
        apartments = Apartment.objects.filter(
            Q(city__icontains=location_query) |
            Q(country__icontains=location_query) |
            Q(address__icontains=location_query)).distinct()

    elif (location_query == None and guests_query != None):
        apartments = Apartment.objects.filter(Q(beds__gte = guests_query)).distinct()

    else:
        apartments = Apartment.objects.all()

    #apartments = Apartment.objects.filter((
     #   Q(city__icontains = location_query) |
      #  Q(country__icontains = location_query) |
       # Q(address__icontains = location_query)) &
        #Q(beds__gte = guests_query)).distinct()
    # ---------------------------------------------------



    # -------------------------------------------------------------
    #Filter basert på start- og sluttdato. Bruker Contract-modul
    #som inneholder en fremmednøkkel som referer til en leilighet:

    #apartments = Apartment.objects.exclude(
     #   (Q(contract__start_date__lte = start_date_query) &
      #  Q(contract__end_date__gte = start_date_query)) |

       # (Q(contract__start_date__lte = end_date_query) &
        #Q(contract__end_date__gte = end_date_query)) |

        #(Q(contract__start_date__gt = start_date_query) &
        #Q(contract__end_date__lt = end_date_query))).distinct()
    # ------------------------------------------------------------

    start_date = start_date_query.split('-')
    start_date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = end_date_query.split('-')
    end_date = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    delta = end_date - start_date

    context = {
        'apartments': apartments,
        'query': {
            'location': location_query,
            'guests': guests_query,
            'start_date': start_date_query,
            'end_date': end_date_query
        },
        'days': delta.days
    }

    return render(request, 'apartments/apartments.html', context)


def apartment_detail(request, apartment_id, start_date, end_date):
    apartment = Apartment.objects.get(pk=apartment_id)

    apartment_price = apartment.calculate_price(start_date, end_date)


    context = {
        'apartment': apartment,
        'query': {
            'start_date': start_date,
            'end_date': end_date
        },
        'apartment_price': apartment_price
    }
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
