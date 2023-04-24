from django.urls import path
from .views import FacultyApiView, FacultyDetailApiView, TicketApiView, TicketDetailApiView


urlpatterns = [
    path('faculties/', FacultyApiView.as_view()),
    path('faculties/<int:pk>/', FacultyDetailApiView.as_view()),
    path('tickets/', TicketApiView.as_view()),
    path('tickets/<int:pk>', TicketDetailApiView.as_view()),
]
