from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

from apartments.models import Apartment
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
        user = Profile.objects.get(pk=request.user.pk)
        user.delete()
        return redirect('landing-page')
