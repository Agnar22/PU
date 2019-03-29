from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.db.models import Count
from apartments.models import Apartment, Contract
from review.models import CompleteReview, ApartmentReview, UserReview
from authentication.forms import RegisterForm, LoginForm
from authentication.models import Profile
from django.db.models import Q
from django.contrib import messages



# Updates the rating of an object (user/apartment in this instance).
# Rated is the rating the current object was rated in the review
def update_rating(object, rated):
    object.update_rating(rated)
    object.save()

def get_review(tenant_pk, subtenant_pk, apartment_pk, contract_pk):
    # for obj in CompleteReview.objects.all():
    #     print('tenant', obj.review_of_tenant.user_to_be_reviewed.pk, tenant_pk, obj.review_of_tenant)
    #     print('subtenant', obj.review_of_subtenant.user_to_be_reviewed.pk, subtenant_pk)
    #     print('apartment', obj.apartment_review.apartment_to_be_reviewed.pk, apartment_pk)
    #     print('contract', obj.contract.pk, contract_pk)
    #     print()
    query_set = CompleteReview.objects.filter(Q(review_of_tenant__user_to_be_reviewed__pk=tenant_pk) &
                                              Q(review_of_subtenant__user_to_be_reviewed__pk=subtenant_pk) &
                                              Q(apartment_review__apartment_to_be_reviewed__pk=apartment_pk) &
                                              Q(contract__pk=contract_pk))
    if len(query_set) > 0:
        return query_set[0]
    return None


def review(request):
    if not request.user.is_authenticated:
        return redirect('landing-page')
    return redirect('landing-page')


def user_and_apartment_review(request, tenant_pk, subtenant_pk, apartment_pk, contract_pk):
    if not request.user.is_authenticated:
        print('not authenticated')
        return redirect('landing-page')

    if request.user.pk == tenant_pk:
        print('tenant is logged in')
        return user_review(request, subtenant_pk, apartment_pk, contract_pk)

    # User_id, apartment_id and authenticated user matches (a matching review model is available)
    print('find', tenant_pk, request.user.pk, apartment_pk, contract_pk)
    active_review = get_review(tenant_pk, request.user.pk, apartment_pk, contract_pk)

    # The requested review does not exist
    if active_review == None:
        messages.error(request, "Noe gikk galt, prøv igjen")
        return HttpResponseRedirect('/profile')
    # It has already been reviewed
    if active_review.apartment_review.has_reviewed:
        messages.warning(request, "Du har allerede gitt denne tilbakemelding!")
        return HttpResponseRedirect('/profile')

    # Get a request form for the subtenant
    if request.method == 'GET':
        print(request.GET.get('value'))
        # return request page
        context = {
            'tenant_first': active_review.review_of_tenant.user_to_be_reviewed.first_name,
            'tenant_last': active_review.review_of_tenant.user_to_be_reviewed.last_name,
            'apartment': active_review.apartment_review.apartment_to_be_reviewed,
            'tenant': tenant_pk,
            'subtenant': subtenant_pk,
            'apartment': apartment_pk,
            'apartment_object': Apartment.objects.get(pk=apartment_pk),
            'contract': contract_pk
        }
        return render(request, 'review/review_user_apartment.html', context)

    # Update review from subtenant
    if request.method == 'POST':
        # Both apartment and tenant is not rated
        if request.POST.get('apartment_rating') == '-1' or request.POST.get('tenant_rating') == '-1':
            context = {
                'tenant_first': active_review.review_of_tenant.user_to_be_reviewed.first_name,
                'tenant_last': active_review.review_of_tenant.user_to_be_reviewed.last_name,
                'apartment': active_review.apartment_review.apartment_to_be_reviewed,
                'tenant': tenant_pk,
                'subtenant': subtenant_pk,
                'apartment': apartment_pk,
                'apartment_object': Apartment.objects.get(pk=apartment_pk),
                'contract': contract_pk
            }
            return render(request, 'review/review_user_apartment.html', context)

        # Review of apartment
        active_review.apartment_review.review = int(request.POST.get('apartment_rating'))
        active_review.apartment_review.has_reviewed = True
        update_rating(active_review.apartment_review.apartment_to_be_reviewed, int(request.POST.get('apartment_rating')))
        active_review.apartment_review.save()

        # Review of tenant
        active_review.review_of_tenant.review = int(request.POST.get('tenant_rating'))
        active_review.review_of_tenant.has_reviewed = True
        update_rating(active_review.review_of_tenant.user_to_be_reviewed, int(request.POST.get('tenant_rating')))
        active_review.review_of_tenant.save()

        # Update active_review if both has reviewed
        if active_review.review_of_tenant.has_reviewed and active_review.review_of_subtenant.has_reviewed:
            active_review.is_finished = True
            active_review.save()
        messages.success(request, "Tilbakemelding sendt!")
        return HttpResponseRedirect('/profile')
    return redirect('landing-page')


# Tenants way of rating subtenant
def user_review(request, subtenant_pk, apartment_pk, contract_pk):
    tenant_pk = request.user.pk
    active_review = get_review(tenant_pk, subtenant_pk, apartment_pk, contract_pk)

    # The requested review does not exist
    if active_review == None:
        messages.error(request, "Noe gikk galt, prøv igjen")
        return HttpResponseRedirect('/profile')

    # It has already been reviewed
    if active_review.review_of_subtenant.has_reviewed:
        messages.warning(request, "Du har allerede gitt denne tilbakemelding!")
        return HttpResponseRedirect('/profile')

    # Get a request form for the subtenant
    if request.method == 'GET':
        # return request page
        context = {
            'subtenant_first': active_review.review_of_subtenant.user_to_be_reviewed.first_name,
            'subtenant_last': active_review.review_of_subtenant.user_to_be_reviewed.last_name,
            'tenant': tenant_pk,
            'subtenant': subtenant_pk,
            'apartment': apartment_pk,
            'apartment_object': Apartment.objects.get(pk=apartment_pk),
            'contract': contract_pk
        }
        return render(request, 'review/review_user.html', context)

    if request.method == 'POST':
        # Subtenant is not rated
        if  request.POST.get('subtenant_rating') == '-1':
            context = {
                'subtenant_first': active_review.review_of_subtenant.user_to_be_reviewed.first_name,
                'subtenant_last': active_review.review_of_subtenant.user_to_be_reviewed.last_name,
                'tenant': tenant_pk,
                'subtenant': subtenant_pk,
                'apartment': apartment_pk,
                'apartment_object': Apartment.objects.get(pk=apartment_pk),
                'contract': contract_pk
            }
            return render(request, 'review/review_user.html', context)

        # Review of subtenant
        active_review.review_of_subtenant.review = int(request.POST.get('subtenant_rating'))
        active_review.review_of_subtenant.has_reviewed = True
        update_rating(active_review.review_of_subtenant.user_to_be_reviewed, int(request.POST.get('subtenant_rating')))
        active_review.review_of_subtenant.save()

        if active_review.review_of_tenant.has_reviewed and active_review.review_of_subtenant.has_reviewed:
            active_review.is_finished = True
            active_review.save()
        messages.success(request, "Tilbakemelding sendt!")
        return HttpResponseRedirect('/profile')

    return redirect('landing-page')