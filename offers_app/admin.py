"""
Django admin configuration for the offers app.

Registers Offer and OfferDetail models and inline admin components.
"""

from django.contrib import admin
from .models import Offer, OfferDetail



class OfferDetailInline(admin.TabularInline):
    model = OfferDetail
    extra = 3
    max_num = 3
    fields = (
        "title",
        "offer_type",
        "price",
        "delivery_time_in_days",
        "revisions",
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    inlines = [OfferDetailInline]
    list_display = ("id", "title", "user", "created_at", "updated_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description", "user__username")
    readonly_fields = ("created_at", "updated_at")


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "offer",
        "offer_type",
        "price",
        "delivery_time_in_days",
    )
    list_filter = ("offer_type",)
    search_fields = ("title", "offer__title")