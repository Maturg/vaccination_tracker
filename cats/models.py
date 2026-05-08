from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime, timedelta

User = get_user_model()

class CHOICES(models.TextChoices):
    GRAY = 'Gray', 'Серый'
    BLACK = 'Black', 'Чёрный'
    WHITE = 'White', 'Белый'
    GINGER = 'Ginger', 'Рыжий'
    MIXED = 'Mixed', 'Смешанный'

# Модель котика (остаётся без изменений)
class Cat(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16, choices=CHOICES.choices)
    birth_year = models.IntegerField(
        validators=[
            MinValueValidator(datetime.now().year - 40),
            MaxValueValidator(datetime.now().year),
        ]
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cats'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_name_owner')
        ]

    def __str__(self):
        return self.name

    @property
    def age(self):
        return datetime.now().year - self.birth_year


# НОВАЯ МОДЕЛЬ: Справочник вакцин
class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название вакцины')
    description = models.TextField(blank=True, verbose_name='Описание')
    validity_period = models.PositiveIntegerField(
        default=365,
        verbose_name='Срок действия (дней)',
        help_text='Через сколько дней после вакцинации нужна ревакцинация'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Вакцина'
        verbose_name_plural = 'Вакцины'
        ordering = ['name']

    def __str__(self):
        return self.name


# НОВАЯ МОДЕЛЬ: Вакцинация кота
class Vaccination(models.Model):
    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, related_name='vaccinations',
        verbose_name='Котик'
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE, related_name='vaccinations',
        verbose_name='Вакцина'
    )
    vaccination_date = models.DateField(verbose_name='Дата вакцинации')
    next_due_date = models.DateField(
        verbose_name='Дата следующей вакцинации',
        help_text='Рассчитывается автоматически: vaccination_date + vaccine.validity_period'
    )
    notes = models.TextField(blank=True, verbose_name='Заметки')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Вакцинация'
        verbose_name_plural = 'Вакцинации'
        ordering = ['-vaccination_date']
        # У одного котика не может быть двух одинаковых вакцин в один день
        unique_together = [['cat', 'vaccine', 'vaccination_date']]

    def __str__(self):
        return f'{self.cat.name} - {self.vaccine.name} ({self.vaccination_date})'

    def save(self, *args, **kwargs):
        # Автоматический расчёт следующей даты вакцинации
        if not self.next_due_date:
            self.next_due_date = self.vaccination_date + timedelta(days=self.vaccine.validity_period)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Просрочена ли вакцинация (следующая дата уже прошла)"""
        return self.next_due_date < datetime.now().date()

    @property
    def days_until_due(self):
        """Дней до следующей вакцинации (отрицательное число если просрочена)"""
        delta = self.next_due_date - datetime.now().date()
        return delta.days