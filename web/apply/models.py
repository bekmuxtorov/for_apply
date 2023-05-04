from django.db import models

# Create your models here.


STATUS_LIST = (
    ('new', 'Yangi'),
    ('waiting', 'Kutilmoqda'),
    ('confirmed', 'Tasdiqlangan'),
)


class Faculty(models.Model):
    name = models.CharField(max_length=200, verbose_name='Fakultet')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'faculty'
        verbose_name = 'Fakultet'
        verbose_name_plural = 'Fakultetlar'

    def get_count(self):
        return self.tickets.count()


class User(models.Model):
    full_name = models.CharField(
        max_length=400,
        verbose_name='Ism, Familiya va Sharif'
    )
    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.SET_NULL,
        verbose_name='Fakultet',
        related_name='tickets',
        blank=True,
        null=True
    )
    group_number = models.CharField(
        max_length=20,
        verbose_name='Guruh'
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name='Telefon raqam'
    )
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.full_name + ' | ' + self.faculty.name


class TicketType(models.Model):
    name = models.CharField(max_length=250, verbose_name='Ariza turi')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'ticket_type'
        verbose_name = 'Ariza Turi'
        verbose_name_plural = 'Ariza Turlari'

    def get_count(self):
        return self.ticket.count()


class Ticket(models.Model):
    type = models.ForeignKey(
        to=TicketType,
        on_delete=models.SET_NULL,
        verbose_name='Ariza turi',
        related_name='ticket',
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Foydalanuvchi',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=13,
        choices=STATUS_LIST,
        default='new'
    )
    file = models.ImageField(
        upload_to='ticket_image/',
        verbose_name='Kvitansiya rasmi',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Ariza matni',
        blank=True,
        null=True
    )
    paynet = models.DecimalField(
        decimal_places=3,
        verbose_name='To\'langan summa',
        max_digits=9
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.full_name + ' || ' + str(self.id)

    def get_date(self):
        return self.created_at.strftime("%H:%M / %d.%m.%Y")

    def get_status(self):
        for i in STATUS_LIST:
            if i[0] == self.status:
                return i[1]

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Ariza'
        verbose_name_plural = 'Arizalar'
