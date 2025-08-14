from django.contrib.auth.models import User
from django.db import models

class Desks(models.Model):
    id = models.AutoField('Номер стола', primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Сотрудник', unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'{self.user}'
