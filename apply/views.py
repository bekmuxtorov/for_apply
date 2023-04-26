from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import models

STATUS_LIST = (
    ('new', 'Yangi'),
    ('waiting', 'Kutilmoqda'),
    ('confirmed', 'Tasdiqlangan'),
)


def get_status(status):
    for i in STATUS_LIST:
        if i[0] == status:
            return i[1]


@login_required
def home_page(request):
    faculties_data = models.Faculty.objects.all().order_by('created_at')
    faculties_name = [faculty_data.name for faculty_data in faculties_data]
    faculties_count = [faculty_data.get_count()
                       for faculty_data in faculties_data]

    context = {
        'status_list': STATUS_LIST,
        'faculties_name': faculties_name,
        'faculties_count': faculties_count
    }
    return render(request, 'index.html', context)


@login_required
def tickets_page(request):
    tickets = models.Ticket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'tables.html', context)


@login_required
def tables_detail(request, pk):
    choose_ticket = models.Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        choose_ticket.status = 'confirmed'
        choose_ticket.save()

    context = {
        'ticket': choose_ticket,
        'status_list': STATUS_LIST
    }
    return render(request, 'detail_ticket.html', context)


@login_required
def status_tables_page(request, status):
    filter_status = models.Ticket.objects.filter(status=status)
    status = get_status(status)
    context = {
        'filter_status': filter_status,
        'status': status
    }
    return render(request, 'filter_tables.html', context)
