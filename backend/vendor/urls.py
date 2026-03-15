from django.urls import path
from .views import VendorListOrCreateView, VendorRetriveUpdateDeleteView

urlpatterns = [
    path("", VendorListOrCreateView.as_view()),
    path("<uuid:pk>/", VendorRetriveUpdateDeleteView.as_view()),
]