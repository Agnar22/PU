import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from apartments.forms import CreateApartmentForm
from authentication.models import Profile
from .models import Apartment
from .models import Contract
from django.db.models import Q


def apartments(request):
    location_query = request.GET.get("location")
    guests_query = request.GET.get("guests")
    start_date_query = request.GET.get("start_date")
    end_date_query = request.GET.get("end_date")

    start_date = start_date_query.split('-')
    start_date = datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2]))
    end_date = end_date_query.split('-')
    end_date = datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2]))
    delta = end_date - start_date

    if (location_query != None and guests_query != None and
            start_date_query != None and end_date_query != None):

        # Returnerer ingenting dersom brukeren
        # har skrevet inn startdato etter sluttdato,
        # eller startdato før dagens dato
        if (start_date_query >= end_date_query
                or start_date_query < datetime.datetime.today().strftime('%Y-%m-%d')):

            apartments = Apartment.objects.none()

        else:
            apartments = Apartment.objects.filter((
                # Filtrer etter lokasjon
                Q(city__icontains=location_query) |
                Q(country__icontains=location_query) |
                Q(address__icontains=location_query)) &

                # Filtrer etter sengeplasser
                Q(beds__gte=guests_query)).exclude(

                # Filtrer etter ledig dato:
                contracts__in=Contract.objects.filter(
                    Q(start_date__lte=start_date.date()) &
                    Q(end_date__gte=start_date.date()))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__lte=end_date.date()) &
                    Q(end_date__gte=end_date.date()))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__gt=start_date.date()) &
                    Q(end_date__lt=end_date.date()))).order_by('beds', 'monthly_cost').distinct()

    # Dersom noe går galt returneres ingenting
    else:
        apartments = Apartment.objects.none()


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
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    error_message = ""

    #Hvis bruker prøver å opprette en ny kontrakt
    if request.method=='POST':

        #Sjekker at brukeren har en apartment som kan opprettes kontrakt på, ved å
        #telle antall ledige leiligheter
        apartment_count = Apartment.objects.filter(pk=apartment_id).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__lte=start_date.date()) &
                Q(end_date__gte=start_date.date()))).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__lte=end_date.date()) &
                Q(end_date__gte=end_date.date()))).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__gt=start_date.date()) &
                Q(end_date__lt=end_date.date()))).order_by('beds', 'monthly_cost').distinct().count()

        #Sjekker at bruker ikke prøver å opprette kontrakt med seg selv
        if not apartment.owner==request.user:

            #Sjekker at det er en ledig apartment
            if apartment_count==1:
                contract = Contract.objects.create(contract_text="", tenant=request.user,
                                                   start_date=start_date, end_date=end_date)

                contract_for_apartment = Apartment.objects.get(pk=apartment_id)
                contract_for_apartment.contracts.add(contract)

                error_message = "Sent contract - Approval pending"

            else:
                error_message = "Contract creation failed - Date not available"
        else:
            error_message = "Contract creation failed - This is your apartment"

    context = {
        'apartment': apartment,
        'query': {
            'start_date': start_date,
            'end_date': end_date
        },
        'apartment_price': apartment_price,
        'owner': apartment.owner,
        'message': error_message}

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


