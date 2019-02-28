from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

from apartments.models import Apartment, Contract
from authentication.models import Profile


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
            if "godkjenn" in request.POST:
                #Godkjenner kontrakten
                contract.pending = False;
                contract.save()

            #Brukeren trykte på avslå
            elif "avslå" in request.POST:
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
