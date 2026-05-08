from django.contrib import admin
from .models import Cat, Achievement, AchievementCat

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'birth_year', 'owner', 'age', 'created_at')
    list_filter = ('color', 'birth_year', 'owner')
    search_fields = ('name', 'owner__username')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(AchievementCat)
class AchievementCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'achievement', 'cat')