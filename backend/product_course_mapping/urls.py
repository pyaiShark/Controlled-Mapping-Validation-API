from django.urls import path
from .views import ProductCourseMappingListOrCreateView, ProductCourseMappingRetriveUpdateDeleteView

urlpatterns = [
    path("", ProductCourseMappingListOrCreateView.as_view()),
    path("<uuid:pk>/", ProductCourseMappingRetriveUpdateDeleteView.as_view()),
]