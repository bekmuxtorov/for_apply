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


def home_page(request):
    context = {'status_list': STATUS_LIST}
    return render(request, 'index.html', context)


def tickets_page(request):
    tickets = models.Ticket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'tables.html', context)


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


def status_tables_page(request, status):
    filter_status = models.Ticket.objects.filter(status=status)
    status = get_status(status)
    context = {
        'filter_status': filter_status,
        'status': status
    }
    return render(request, 'filter_tables.html', context)
