import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

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
    status_count = 

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
    msg = str()
    choose_ticket = models.Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        choose_ticket.status = 'confirmed'
        choose_ticket.save()
        msg = 'Ariza muaffiqiyatli tasdiqlandi'

    context = {
        'ticket': choose_ticket,
        'status_list': STATUS_LIST,
        'msg': msg
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


def send_message(telegram_id, message):
    TOKEN = settings.BOT_TOKEN
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, {'chat_id': telegram_id,
                  'text': message, 'parse_mode': 'HTML'})


@login_required
def send_message_page(request, pk):
    choose_ticket = models.Ticket.objects.get(pk=pk)
    tickets = models.Ticket.objects.all().order_by('-created_at')[:10]
    student_name = choose_ticket.full_name.split(' ')[0]
    message = f'Assalomu alekum {student_name.title()}\n\n'
    msg = str()
    if request.method == 'POST':
        subject = request.POST.get('subject')
        text = request.POST.get('text')
        message += f'<b>Mavzu:</b> {subject}\n'
        message += f'<b>Xabar:</b> {text}'
        send_message(choose_ticket.telegam_id, message)
        msg = 'Xabar muvaffaqiyat yuborildi!'
    context = {
        'tickets': tickets,
        'choose_ticket': choose_ticket,
        'msg': msg
    }
    return render(request, 'send_message.html', context)
