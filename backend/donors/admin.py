from django.contrib import admin
from .models import Donor
# Register your models here.

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):

    list_display = (
        "donor_id",
        "name",
        "blood_group",
        "city",
        "eligible_date",
        "donation_count",
    )

    search_fields = (
        "donor_id",
        "name",
        "email",
        "phone",
    )

    list_filter = (
        "blood_group",
        "city",
        "state",
    )

    