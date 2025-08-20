from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Desks(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Сотрудник', unique=True, related_name='desk')
    number = models.PositiveSmallIntegerField('Номер стола', unique=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'

    def __str__(self):
        return f'{self.number}: {self.user.profile}'

    def clean(self):
        current_user = self.user.profile.tester
        neigh1 = Desks.objects.filter(number=self.number - 1).first()
        neigh2 = Desks.objects.filter(number=self.number + 1).first()
        if neigh1:
            if neigh1.user.profile.tester != current_user:
                raise ValidationError('Тестировщики и разработчики не должны сидеть за соседними столами.')
        if neigh2:
            if neigh2.user.profile.tester != current_user:
                raise ValidationError('Тестировщики и разработчики не должны сидеть за соседними столами.')
