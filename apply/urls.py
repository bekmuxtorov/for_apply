from django.urls import path
from .views import FacultyApiView, TicketApiView


urlpatterns = [
    path('faculties/', FacultyApiView.as_view()),
    path('tickets/', TicketApiView.as_view()),
]
