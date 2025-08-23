from django.contrib.auth.models import User
from django.db.models import Max
from datetime import date
from django.db import models


class UserProfile(models.Model):
    GENDER_CHOICES = {
        0: 'не указан',
        1: 'мужской',
        2: 'женский',
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='profile')
    gender = models.SmallIntegerField('Пол', choices=GENDER_CHOICES, default=0)
    family = models.CharField('Фамилия', max_length=30)
    name = models.CharField('Имя', max_length=30)
    surname = models.CharField('Отчество', max_length=30, blank=True)
    description = models.TextField('Описание', blank=True)
    tester = models.BooleanField('Тестировщик', default=False)
    date = models.DateField('Дата приема', default=date.today)

    @property
    def diff_date(self):
        return (date.today() - self.date).days

    class Meta:
        ordering = ['-date',]
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.family} {self.name}'

class SkillList(models.Model):
    skill = models.CharField('Название', unique=True)

    class Meta:
        verbose_name = 'Навыки'
        verbose_name_plural = 'Список навыков'

    def __str__(self):
        return self.skill

class Skills(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='skills')
    skill = models.ForeignKey(SkillList, on_delete=models.CASCADE, verbose_name='Навык', related_name='users')
    level = models.SmallIntegerField('Уровень освоения', choices=[(a, a) for a in range(1, 11)])

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return f'{self.skill}: {self.level}'

class Gallery(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Сотрудник', related_name='gallery')
    image = models.ImageField('Изображение')
    position = models.PositiveSmallIntegerField('Позиция', default=0)

    class Meta:
        ordering = ['position',]
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея'

    def save(self, *args, **kwargs):
        if not self.position:
            last_position = Gallery.objects.filter(user=self.user).aggregate(Max('position'))['position__max']
            self.position = 1 if last_position is None else last_position + 1
        super().save(*args, **kwargs)