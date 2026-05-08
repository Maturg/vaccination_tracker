from django.contrib import admin
from .models import Cat, Vaccine, Vaccination

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'birth_year', 'owner', 'age')
    list_filter = ('color', 'owner')
    search_fields = ('name', 'owner__username')

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'validity_period', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'cat', 'vaccine', 'vaccination_date', 'next_due_date', 'is_overdue', 'days_until_due')
    list_filter = ('vaccine', 'vaccination_date')
    search_fields = ('cat__name', 'vaccine__name')
    readonly_fields = ('next_due_date',)

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Просрочена'

    def days_until_due(self, obj):
        return obj.days_until_due
    days_until_due.short_description = 'Дней до срока'