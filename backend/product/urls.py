from django.urls import path
from .views import ProductListOrCreateView, ProductRetriveUpdateDeleteView

urlpatterns = [
    path("", ProductListOrCreateView.as_view()),
    path("<uuid:pk>/", ProductRetriveUpdateDeleteView.as_view()),
]