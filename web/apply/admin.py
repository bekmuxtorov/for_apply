from django.contrib import admin
from .models import Faculty, Ticket, TicketType, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'faculty', 'group_number',
                    'phone_number', 'telegram_id', 'created_at')
    search_fields = ('full_name', 'faculty')
    list_filter = ('faculty', 'group_number')


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'type', 'get_faculty',
                    'get_group_number', 'paynet', 'status')

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Ism, Familiya va Otasin ismi'

    def get_faculty(self, obj):
        return obj.user.faculty
    get_faculty.short_description = 'Fakultet nomi'

    def get_group_number(self, obj):
        return obj.user.group_number
    get_group_number.short_description = 'Guruh raqami'
