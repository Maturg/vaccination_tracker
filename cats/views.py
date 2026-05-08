from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import filters
from .models import Cat, Achievement
from .serializers import CatSerializer, AchievementSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import get_user_model

User = get_user_model()

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all().order_by('-created_at')
    serializer_class = CatSerializer
    permission_classes = [IsOwnerOrReadOnly]
    #filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    #filterset_fields = ['color', 'birth_year']
    #search_fields = ['name']
    #ordering_fields = ['name', 'birth_year', 'created_at']
    #ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], url_path='recent-white')
    def recent_white_cats(self, request):
        cats = Cat.objects.filter(color='White').order_by('-created_at')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer