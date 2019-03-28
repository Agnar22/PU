import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.db.models import Count
from apartments.models import Apartment
from authentication.forms import RegisterForm, LoginForm
from authentication.models import Profile
from apartments.models import Apartment, Contract
from review.models import CompleteReview, UserReview, ApartmentReview
from django.contrib import messages
from django.db.models import Q


def contract_apartments_match(contract, apartments):
    for apartment in apartments.all():
        if contract in apartment.contracts.all():
            return apartment
    return None


# Finding expired contracts that are not yet used in a review
def filter_contracts():
    contracts_set = Contract.objects.filter(Q(review_made=False) & Q(pending=False))
    contracts = [contract for contract in contracts_set if contract.end_date < datetime.datetime.today().date()]
    for contract in contracts:
        contract.review_made = True
        contract.save()
    all_apartments = Apartment.objects.all()
    apartments = [contract_apartments_match(contract, all_apartments) for contract in contracts]
    return contracts, apartments


# Sending email with url
def send_email(mail, url):
    pass


# Creating new review models for expired contracts
def create_review_models():
    contracts, apartments = filter_contracts()
    for x in range(len(contracts)):
        print(contracts[x], apartments[x])
        subtenant_review = UserReview.objects.create(user_to_be_reviewed=contracts[x].tenant,
                                                     user_to_review=apartments[x].owner)
        tenant_review = UserReview.objects.create(user_to_be_reviewed=apartments[x].owner,
                                                  user_to_review=contracts[x].tenant)
        apartment_review = ApartmentReview.objects.create(apartment_to_be_reviewed=apartments[x],
                                                          user_to_review=contracts[x].tenant)
        CompleteReview.objects.create(apartment_review=apartment_review,
                                      review_of_tenant=tenant_review,
                                      review_of_subtenant=subtenant_review,
                                      contract=contracts[x])
        url = "https://sharebnb.herokuapp.com/to_review/" + str(apartments[x].owner.pk) + "/" + str(contracts[x].tenant.pk)\
                                                    + "/" + str(apartments[x].pk) + "/" + str(contracts[x].pk)
        send_email(contracts[x].tenant.email, url)
        send_email(apartments[x].owner.email, url)


def landing_page(request):
    create_review_models()
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

    else:  # POST
        if request.POST.get("first_name"):  # Register
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
