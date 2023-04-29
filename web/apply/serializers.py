from rest_framework import serializers
from .models import Faculty, Ticket


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = '__all__'
