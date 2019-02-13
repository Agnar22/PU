from django.shortcuts import render


def profile_view(request):
    return render(request, 'profile_page/profile-page.html', {})
