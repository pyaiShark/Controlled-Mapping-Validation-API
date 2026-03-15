from django.urls import path
from .views import CertificationListOrCreateView, CertificationRetriveUpdateDeleteView

urlpatterns = [
    path("", CertificationListOrCreateView.as_view()),
    path("<uuid:pk>/", CertificationRetriveUpdateDeleteView.as_view()),
]