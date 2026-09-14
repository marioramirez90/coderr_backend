from django.urls import path
from .views import (
    OfferListCreateView,
    OfferDetailView,
    SingleOfferDetailView,
    BaseInfoView,
)

urlpatterns = [
    path("offers/", OfferListCreateView.as_view(), name="offer-list-create"),
    path("offers/<int:pk>/", OfferDetailView.as_view(), name="offer-detail"),
    path("offerdetails/<int:pk>/", SingleOfferDetailView.as_view(), name="single-offer-detail"),
    
    path("base-info/", BaseInfoView.as_view(), name="base-info"),
]