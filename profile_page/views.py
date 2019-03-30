from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

import datetime

from apartments.models import Apartment, Contract
from authentication.forms import RegisterForm
from authentication.models import Profile
from django.db.models import Q
from django.contrib import messages

from emails.emails import send_review_email


def profile_view(request):

    # Sletter ugyldige kontraktforespørsler
    invalid_requests = Contract.objects.filter(
        Q(start_date__lt=datetime.datetime.today().strftime('%Y-%m-%d')) &
        (Q(pending=True) |
         Q(owner_approved=False))
        ).delete()

    if request.user.is_authenticated:
        my_rented_apartments = Apartment.objects.filter(
            Q(contracts__tenant__email__iexact=request.user.email) |
            Q(contracts__tenants__contains=request.user.email)).distinct()

        has_rented_apartments = my_rented_apartments.count() > 0
        owns_apartments = Apartment.objects.filter(owner=request.user).count() > 0

        context = {
            'form': RegisterForm(),
            'my_apartments': Apartment.objects.filter(owner=request.user),
            'my_rented_apartments': my_rented_apartments,
            'has_rented_apartments': has_rented_apartments,
            'owns_apartments': owns_apartments,
            'owner_of': Apartment.objects.filter(Q(original_owner__iexact=request.user.email))
        }

    if request.method == 'GET':
        if not request.user.is_authenticated:
            messages.warning(request, "Du må logge inn først")
            return redirect('landing-page')
        else:
            return render(request, 'profile_page/profile-page.html', context)

    else:  # POST
        contract_id = request.POST.get("contract_id")

        if "first_name" in request.POST:
            user = Profile.objects.get(pk=request.user.pk)
            form = RegisterForm(request.POST, instance=user)
            user.first_name = form['first_name'].data
            user.last_name = form['last_name'].data
            user.phone_number = int(form['phone_number'].data)
            user.save()

            return render(request, 'profile_page/profile-page.html', context)

        elif contract_id is not None:
            contract = Contract.objects.get(pk=contract_id)
            apartment_id = Apartment.objects.get(contracts__pk=contract_id).pk

            # Brukeren er utleier og trykte på godkjenn fremleie
            if "accept_owner" in request.POST:
                # Godkjenner kontrakten
                contract.owner_approved = True
                contract.save()

            # Brukeren er fremleier og trykte på godkjenn
            elif "accept" in request.POST:
                # Godkjenner kontrakten
                contract.pending = False;
                start_date_accepted = contract.start_date
                end_date_accepted = contract.end_date
                contract.save()

                Contract.objects.filter(
                    apartment=apartment_id).exclude(

                    Q(pk=contract_id)).filter(

                    Q(pending=True) &

                    (Q(start_date__lte=start_date_accepted) &
                    Q(end_date__gte=start_date_accepted)) |

                    (Q(start_date__lte=end_date_accepted) &
                    Q(end_date__gte=end_date_accepted)) |

                    (Q(start_date__gt=start_date_accepted) &
                    Q(end_date__lt=end_date_accepted))).delete()

            # Brukeren trykte på avslå
            elif "decline" in request.POST:
                contract.delete()

        # Viser profilsiden dersom brukeren fremdeles er logget inn
        if request.user.is_authenticated:
            return render(request, 'profile_page/profile-page.html', context)
        else:
            messages.warning(request, "Du må logge inn først")
            return redirect('landing-page')


def delete_user(request):
    # Oppdaterer alle kontraktene og leilighetene slik at de ikke lenger har en
    # utleier/eier
    contracts = Contract.objects.filter(Q(apartment__original_owner__iexact=request.user.email))
    contracts.update(owner_approved=True)
    owner_of = Apartment.objects.filter(original_owner=request.user.email)
    owner_of.update(original_owner=None)

    # Sletter brukeren
    user = Profile.objects.get(pk=request.user.pk)
    user.delete()
    return redirect('landing-page')