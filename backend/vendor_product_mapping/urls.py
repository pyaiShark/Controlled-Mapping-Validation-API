from django.urls import path
from .views import VendorProductMappingListOrCreateView, VendorProductMappingRetriveUpdateDeleteView

urlpatterns = [
    path("", VendorProductMappingListOrCreateView.as_view()),
    path("<uuid:pk>/", VendorProductMappingRetriveUpdateDeleteView.as_view()),
]