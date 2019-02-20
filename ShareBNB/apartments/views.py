from django.shortcuts import render

# Create your views here.

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


    context = {
        'apartments': apartments
    }

    return render(request, 'apartments/apartments.html', context)


def apartment_detail(request, apartment_id):
    context = {'id': apartment_id}
    return render(request, 'apartments/apartment-detail.html', context)


