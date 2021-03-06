import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from emails.emails import send_review_email

from django.db.models import Count
from apartments.models import Apartment
from authentication.forms import RegisterForm, LoginForm
from authentication.models import Profile
from apartments.models import Apartment, Contract
from review.models import CompleteReview, UserReview, ApartmentReview
from django.contrib import messages
from django.db.models import Q


def contract_apartments_match(contract):
    try:
        return Apartment.objects.get(Q(contracts__in=[contract]))
    except:
        return None

# Finding expired contracts that are not yet used in a review
def filter_contracts():
    contracts = Contract.objects.filter(
        Q(review_made=False) &
        Q(pending=False) &
        Q(owner_approved=True) &
        Q(end_date__lt=datetime.datetime.today().strftime('%Y-%m-%d')))

    return contracts

# Sending email with url
def send_email(receiver, url):
    send_review_email(url, receiver)


# Creating new review models for expired contracts
def create_review_models():
    contracts = filter_contracts()
    for contract in contracts:
        apartment = contract_apartments_match(contract)
        if apartment is not None:
            subtenant_review = UserReview.objects.create(user_to_be_reviewed=contract.tenant,
                                                         user_to_review=apartment.owner)
            tenant_review = UserReview.objects.create(user_to_be_reviewed=apartment.owner,
                                                      user_to_review=contract.tenant)
            apartment_review = ApartmentReview.objects.create(apartment_to_be_reviewed=apartment,
                                                              user_to_review=contract.tenant)
            CompleteReview.objects.create(apartment_review=apartment_review,
                                          review_of_tenant=tenant_review,
                                          review_of_subtenant=subtenant_review,
                                          contract=contract)
            url = "https://sharebb.herokuapp.com/to_review/" + str(apartment.owner.pk) + "/" + str(contract.tenant.pk) \
                  + "/" + str(apartment.pk) + "/" + str(contract.pk)
            send_email(contract.tenant.email, url)
            send_email(apartment.owner.email, url)

    contracts.update(review_made=True)

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
            form = RegisterForm(request.POST, request.FILES or None)
            if form.is_valid():
                user = form.save(commit=False)

                # Cleaned (normalized) data
                email = form.cleaned_data['email'].lower()
                password = form.cleaned_data['password']
                user.set_password(password)
                try:
                    image = request.FILES.get("image")
                    if image is not None:
                        user.profile_picture = image
                    user.save()
                except:
                    messages.error(request, 'Noe gikk galt, prøv igjen')
                    return redirect('/')



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
