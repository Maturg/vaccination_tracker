from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cat, Vaccine, Vaccination

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    age = serializers.ReadOnlyField()

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'age', 'created_at')


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ('id', 'name', 'description', 'validity_period', 'is_active')


class VaccinationSerializer(serializers.ModelSerializer):
    cat_name = serializers.ReadOnlyField(source='cat.name')
    vaccine_name = serializers.ReadOnlyField(source='vaccine.name')
    is_overdue = serializers.ReadOnlyField()
    days_until_due = serializers.ReadOnlyField()
    next_due_date = serializers.ReadOnlyField()  # <--- ДОБАВЬТЕ ЭТУ СТРОКУ

    class Meta:
        model = Vaccination
        fields = ('id', 'cat', 'cat_name', 'vaccine', 'vaccine_name',
                  'vaccination_date', 'next_due_date', 'notes',
                  'is_overdue', 'days_until_due')