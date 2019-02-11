from django.shortcuts import render

# Create your views here.


def apartments(request):
    context = {}
    return render(request, 'apartments/apartments.html', context)


def apartment_detail(request):
    context = {}
    return render(request, 'apartments/apartment-detail.html', context)
