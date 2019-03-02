from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

from apartments.models import Apartment, Contract
from authentication.models import Profile
from django.db.models import Q


def profile_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            context = {
                'my_apartments': Apartment.objects.filter(owner=request.user)
            }
            return render(request, 'profile_page/profile-page.html', context)
        else:
            return redirect('landing-page')

    else: # POST
        contract_id = request.POST.get("contract_id")

        if contract_id is not None:
            contract = Contract.objects.get(pk=contract_id)

            #Brukeren trykte på godkjenn
            if "accept" in request.POST:
                #Godkjenner kontrakten
                contract.pending = False;
                start_date_accepted = contract.start_date
                end_date_accepted = contract.end_date
                contract.save()

                Contract.objects.exclude(
                    Q(pk=contract_id)).filter(

                    Q(pending=True) &

                    (Q(start_date__lte=start_date_accepted) &
                    Q(end_date__gte=start_date_accepted)) |

                    (Q(start_date__lte=end_date_accepted) &
                    Q(end_date__gte=end_date_accepted)) |

                    (Q(start_date__gt=start_date_accepted) &
                    Q(end_date__lt=end_date_accepted))).delete()


            #Brukeren trykte på avslå
            elif "decline" in request.POST:
                contract.delete()

            #Viser profilsiden dersom brukeren fremdeles er logget inn
            if request.user.is_authenticated:
                context = {
                    'my_apartments': Apartment.objects.filter(owner=request.user)
                }
                return render(request, 'profile_page/profile-page.html', context)
            else:
                return redirect('landing-page')


        #Dersom brukeren trykker på knappen "slett bruker"
        else:
            user = Profile.objects.get(pk=request.user.pk)
            user.delete()
            return redirect('landing-page')
