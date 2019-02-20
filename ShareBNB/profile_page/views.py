from django.shortcuts import render
from django.http import HttpResponseForbidden

from apartments.models import Apartment

def profile_view(request):
    if request.user.is_authenticated:
        context = {
            'my_apartments': Apartment.objects.filter(owner=request.user)
        }
        print(context['my_apartments'])
        return render(request, 'profile_page/profile-page.html', context)
    else:
        return HttpResponseForbidden()
