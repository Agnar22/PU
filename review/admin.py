from django.contrib import admin

from .models import ApartmentReview, UserReview, CompleteReview


class ApartmentReviewAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    readonly_fields = ('id',)
    fields = ('apartment_to_be_reviewed', 'user_to_review', 'review', 'has_reviewed')

    class Meta:
        model = ApartmentReview


class UserReviewAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    fields = ('user_to_be_reviewed', 'user_to_review', 'review', 'has_reviewed')

    class Meta:
        model = UserReview


class CompleteReviewAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    readonly_fields = ('id',)
    fields = ('apartment_review', 'review_of_tenant', 'review_of_subtenant', 'contract', 'is_finished')

    class Meta:
        model = CompleteReview


admin.site.register(ApartmentReview, ApartmentReviewAdmin)
admin.site.register(UserReview, UserReviewAdmin)
admin.site.register(CompleteReview, CompleteReviewAdmin)
