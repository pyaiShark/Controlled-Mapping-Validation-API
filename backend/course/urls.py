from django.urls import path
from .views import CourseListOrCreateView, CourseRetriveUpdateDeleteView

urlpatterns = [
    path("", CourseListOrCreateView.as_view()),
    path("<uuid:pk>/", CourseRetriveUpdateDeleteView.as_view()),
]