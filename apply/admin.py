from django.contrib import admin
from .models import Faculty, Ticket

# Register your models here.


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'faculty', 'status', 'created_at')
    search_fields = ('full_name', 'faculty')
    list_filter = ('faculty', 'status')
