from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Ticket, Faculty
from .serializers import FacultySerializer, TicketSerializer


class TicketApiView(ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDetailApiView(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class FacultyApiView(ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyDetailApiView(RetrieveAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
