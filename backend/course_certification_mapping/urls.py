from django.urls import path
from .views import CourseCertificationMappingListOrCreateView, CourseCertificationMappingRetriveUpdateDeleteView

urlpatterns = [
    path("", CourseCertificationMappingListOrCreateView.as_view()),
    path("<uuid:pk>/", CourseCertificationMappingRetriveUpdateDeleteView.as_view()),
]