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


class Ticket(models.Model):
    full_name = models.CharField(
        max_length=400,
        verbose_name='Ism, Familiya va Sharif'
    )
    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.CASCADE,
        verbose_name='Fakultet',
        related_name='tickets'
    )
    group_number = models.CharField(
        max_length=20,
        verbose_name='Guruh'
    )
    status = models.CharField(
        max_length=13,
        choices=STATUS_LIST,
        default='new'
    )
    file = models.ImageField(
        upload_to='ticket_image/',
        verbose_name='Kvitansiya rasmi'
    )
    telegam_id = models.BigIntegerField(verbose_name='Telegram ID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name + ' || ' + str(self.id)

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
