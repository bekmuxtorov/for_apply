from django.db import models

# Create your models here.


STATUS_LIST = (
    ('progress', 'Jarayonda'),
    ('confirmed', 'Tasdiqlangan'),
    ('not_confirmed', 'Tasdiqlanmagan'),
    ('closed', 'Yopildi')
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


class Ticket(models.Model):
    id = models.IntegerField(
        primary_key=True,
        default=10000
    )
    full_name = models.CharField(
        max_length=400,
        verbose_name='Ism, Familiya va Sharif'
    )
    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.CASCADE,
        verbose_name='Fakultet'
    )
    group_number = models.CharField(
        max_length=20,
        verbose_name='Guruh'
    )
    status = models.CharField(
        max_length=13,
        choices=STATUS_LIST,
        default='progress'
    )
    file = models.ImageField(
        upload_to='ticket_image/',
        verbose_name='Kvitansiya rasmi'
    )
    telegam_id = models.BigIntegerField(verbose_name='Telegram ID')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name + ' || ' + str(self.id)

    class Meta:
        db_table = 'ticket'
        verbose_name = 'Ariza'
        verbose_name_plural = 'Arizalar'
