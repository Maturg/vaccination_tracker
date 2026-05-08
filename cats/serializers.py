import base64
import datetime as dt
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cat, Achievement, AchievementCat, CHOICES

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name')

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)

class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)
    color = serializers.ChoiceField(choices=CHOICES.choices)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    age = serializers.ReadOnlyField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements', 'age', 'image', 'created_at')

    def validate_birth_year(self, value):
        year = dt.datetime.now().year
        if not (year - 40 < value <= year):
            raise serializers.ValidationError('Проверьте год рождения!')
        return value

    def validate(self, data):
        if data.get('color') == data.get('name'):
            raise serializers.ValidationError('Имя не может совпадать с цветом!')
        return data

    def create(self, validated_data):
        achievements_data = validated_data.pop('achievements', [])
        cat = Cat.objects.create(**validated_data)
        for achievement_data in achievements_data:
            achievement, _ = Achievement.objects.get_or_create(**achievement_data)
            AchievementCat.objects.create(achievement=achievement, cat=cat)
        return cat

    def update(self, instance, validated_data):
        achievements_data = validated_data.pop('achievements', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if achievements_data is not None:
            instance.achievements.clear()
            for achievement_data in achievements_data:
                achievement, _ = Achievement.objects.get_or_create(**achievement_data)
                AchievementCat.objects.create(achievement=achievement, cat=instance)

        instance.save()
        return instance