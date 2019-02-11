from django.shortcuts import render

# Create your views here.


def apartments(request):
    context = {}
    return render(request, 'apartments/apartments.html', context)


def apartment_detail(request, apartment_id):
    context = {'id': apartment_id}
    return render(request, 'apartments/apartment-detail.html', context)
