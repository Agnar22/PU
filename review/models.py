from django.db import models
from authentication.models import Profile
from apartments.models import Apartment, Contract


# Class to review a user
class UserReview(models.Model):
    user_to_be_reviewed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviewed")
    user_to_review = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviewer")
    review = models.IntegerField(default=-1)
    has_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return '' + str(self.user_to_be_reviewed.email) + ' - ' + str(self.user_to_review.email) + ' - ' + \
               str(self.review) + ' - ' + str(self.has_reviewed)


# Class to review an apartment
class ApartmentReview(models.Model):
    apartment_to_be_reviewed = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="apartment")
    user_to_review = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="subtenant_to_review")
    review = models.IntegerField(default=-1)
    has_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return '' + str(self.apartment_to_be_reviewed.pk) + ' - ' + str(self.user_to_review.email) + ' - ' + \
               str(self.review) + ' - ' + str(self.has_reviewed)


# Class for reviews, one for each ended contract.
class CompleteReview(models.Model):
    apartment_review = models.ForeignKey(ApartmentReview, on_delete=models.CASCADE, related_name="apartment_review")
    review_of_tenant = models.ForeignKey(UserReview, on_delete=models.CASCADE, related_name="tenant_review")
    review_of_subtenant = models.ForeignKey(UserReview, on_delete=models.CASCADE, related_name="subtenant_review")
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name="contract")
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return '' + str(self.apartment_review.__str__()) + ' - ' + str(self.review_of_tenant.__str__()) + ' - ' \
               + str(self.review_of_subtenant.__str__()) + ' - ' + str(self.contract.pk) + ' - ' + str(self.is_finished)
