import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from apartments.forms import CreateApartmentForm, CreateContractForm
from authentication.models import Profile
from .models import Apartment, ApartmentImage
from .models import Contract
from django.db.models import Q
from geopy.geocoders import Nominatim
from django.contrib import messages


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
            apartments_map = Apartment.objects.none()
            messages.error(request, "Ugyldig dato!")

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
                    Q(end_date__gte=start_date.date()) &
                    Q(pending=False))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__lte=end_date.date()) &
                    Q(end_date__gte=end_date.date()) &
                    Q(pending=False))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__gt=start_date.date()) &
                    Q(end_date__lt=end_date.date()) &
                    Q(pending=False))).order_by('beds', 'monthly_cost').distinct()


            #Leilighetene som skal vises på kartet skal ikke filtreres etter plassering
            apartments_map = Apartment.objects.filter(

                # Filtrer etter sengeplasser
                Q(beds__gte=guests_query)).exclude(

                #De som mangler koordinater kan ikke vises på kartet
                Q(longitude__isnull=True)).exclude(
                Q(latitude__isnull=True)).exclude(

                # Filtrer etter ledig dato:
                contracts__in=Contract.objects.filter(
                    Q(start_date__lte=start_date.date()) &
                    Q(end_date__gte=start_date.date()) &
                    Q(pending=False))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__lte=end_date.date()) &
                    Q(end_date__gte=end_date.date()) &
                    Q(pending=False))).exclude(

                contracts__in=Contract.objects.filter(
                    Q(start_date__gt=start_date.date()) &
                    Q(end_date__lt=end_date.date()) &
                    Q(pending=False))).order_by('beds', 'monthly_cost').distinct()


    # Dersom noe går galt returneres ingenting
    else:
        apartments = Apartment.objects.none()
        apartments_map = Apartment.objects.none()
        messages.error(request, "Noe gikk galt!")


    geolocator = Nominatim(user_agent="Apartment")
    location = geolocator.geocode(location_query)

    #Setter kartet til byen som ble søkt på
    if location is not None:
        lat = location.latitude
        lon = location.longitude
        zoom = 12

    else:
        lat = 55
        lon = 25
        zoom = 2

    context = {
        'apartments': apartments,
        'apartments_map': apartments_map,
        'query': {
            'location': location_query,
            'guests': guests_query,
            'start_date': start_date_query,
            'end_date': end_date_query
        },
        'days': delta.days,
        'latitude': str(lat),
        'longitude': str(lon),
        'zoom': str(zoom)
    }

    print((lat, lon, zoom))
    return render(request, 'apartments/apartments.html', context)



def apartment_detail(request, apartment_id, start_date, end_date):

    apartment = Apartment.objects.get(pk=apartment_id)

    apartment_price = apartment.calculate_price(start_date, end_date)
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    emails = []

    #Hvis bruker prøver å opprette en ny kontrakt
    if request.method=='POST':
        user_email = request.user.email

        #Sjekker at brukeren har en apartment som kan opprettes kontrakt på, ved å
        #telle antall ledige leiligheter
        apartment_count = Apartment.objects.filter(pk=apartment_id).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__lte=start_date.date()) &
                Q(end_date__gte=start_date.date()) &
                Q(pending=False))).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__lte=end_date.date()) &
                Q(end_date__gte=end_date.date()) &
                Q(pending=False))).exclude(

            contracts__in=Contract.objects.filter(
                Q(start_date__gt=start_date.date()) &
                Q(end_date__lt=end_date.date()) &
                Q(pending=False))).order_by('beds', 'monthly_cost').distinct().count()


        # Får tak i email-adressene til de brukerene brukeren leier sammen med
        form = CreateContractForm(request.POST)
        valid_form = form.is_valid()
        if valid_form:
            #Fjerner alle duplikate emailer, og fjerner brukerens egen email-adresse dersom den ble skrevet inn
            emails = list(dict.fromkeys(form.cleaned_data["tenants"]))
            emails = [x.lower() for x in emails]
            while user_email.lower() in emails:
                emails.remove(user_email.lower())

        # Sjekker om brukeren har sendt en slik kontraktforespørsel tidligere
        contract_count = Contract.objects.filter(
                Q(apartment=apartment_id) &
                Q(start_date__exact=start_date.date()) &
                Q(end_date__exact=end_date.date()) &
                Q(pending=True) &
                (Q(tenants__contains=user_email) |
                 Q(tenant__email__iexact=user_email))).distinct().count()


        if apartment.owner==request.user or apartment.original_owner==user_email:
            messages.error(request, "Dette er din leilighet!")

        elif apartment_count!=1 or start_date >= end_date or start_date.date() < datetime.datetime.today().date():
            messages.error(request, "Datoen er ikke tilgjengelig!")

        elif not valid_form:
            messages.error(request, "Email-adressene er ugyldige!")

        elif apartment.owner.email in emails or apartment.original_owner in emails:
            messages.error(request, "Eier kan ikke leie sin egen leilighet!")

        elif contract_count > 0:
            messages.error(request, "Du har allerede sendt denne forespørselen!")

        else:
            owner_approved = Apartment.objects.get(pk=apartment_id).original_owner is None

            contract = Contract.objects.create(contract_text="", tenant=request.user,
                                               tenants=emails, pending=True, owner_approved=owner_approved,
                                               start_date=start_date, end_date=end_date)

            contract_for_apartment = Apartment.objects.get(pk=apartment_id)
            contract_for_apartment.contracts.add(contract)

            messages.success(request, "Forespørsel om kontrakt er sendt!")


    context = {
        'apartment': apartment,
        'query': {
            'start_date': start_date,
            'end_date': end_date
        },
        'apartment_price': apartment_price,
        'owner': apartment.owner,
        'form': CreateContractForm()}

    return render(request, 'apartments/apartment-detail.html', context)


def create_apartment(request):
    if request.method == 'GET':
        form = CreateApartmentForm()
        return render(request, 'apartments/create-apartment.html', {'form': form})
    elif request.method == 'POST':
        original_owner = None
        owner_count = 0

        geolocator = Nominatim(user_agent="Apartment")

        form = CreateApartmentForm(request.POST, request.FILES or None)
        print(form.errors)

        # Form.is_valid() må kalles for at cleaned_data skal funke
        if form.is_valid():
            original_owner = form.cleaned_data["original_owner"]

            if original_owner == request.user.email:
                original_owner = None

            if original_owner is not None:
                original_owner = original_owner.lower()
                owner_count = Profile.objects.filter(Q(email__iexact=original_owner)).count()

        if form.is_valid() and len(request.FILES.getlist('images')) <= 21 and (original_owner is None or owner_count == 1):
            apartment = form.save(commit=False)
            apartment.owner = Profile.objects.get(pk=request.user.pk)
            apartment.original_owner = original_owner
            apartment.city = apartment.city.lower().capitalize()
            files = request.FILES.getlist('images')

            # Oppretter og lagrer longitude og latitude til adressen
            location = geolocator.geocode(apartment.address + " " + apartment.city + " " + apartment.country)
            if location is not None:
                apartment.latitude = str(location.latitude)
                apartment.longitude = str(location.longitude)

            apartment.save()


            for f in files:
                image = ApartmentImage.objects.create(image=f, image_for=apartment)

            return redirect('profile')
        else:
            print('failed')
            return render(request, 'apartments/create-apartment.html', {'form': form})


