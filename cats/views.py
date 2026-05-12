from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cat, Vaccine, Vaccination
from .serializers import CatSerializer, VaccineSerializer, VaccinationSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly


class CatViewSet(viewsets.ModelViewSet):
    """ViewSet для котиков"""
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VaccineViewSet(viewsets.ModelViewSet):
    """ViewSet для справочника вакцин (только для администратора)"""
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAdminOrReadOnly]


class VaccinationViewSet(viewsets.ModelViewSet):
    """ViewSet для вакцинаций"""
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vaccine', 'cat']

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        """Просроченные вакцинации (next_due_date < сегодня)"""
        today = timezone.now().date()
        overdue_vaccinations = self.queryset.filter(next_due_date__lt=today)
        serializer = self.get_serializer(overdue_vaccinations, many=True)
        return Response({
            'count': overdue_vaccinations.count(),
            'results': serializer.data
        })

    @action(detail=False, methods=['get'], url_path='upcoming')
    def upcoming(self, request):
        """Скоро нужные вакцинации (следующие 30 дней)"""
        today = timezone.now().date()
        upcoming_date = today + timedelta(days=30)
        upcoming_vaccinations = self.queryset.filter(
            next_due_date__gte=today,
            next_due_date__lte=upcoming_date
        ).order_by('next_due_date')
        serializer = self.get_serializer(upcoming_vaccinations, many=True)
        return Response({
            'count': upcoming_vaccinations.count(),
            'results': serializer.data
        })

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        """История вакцинаций конкретного котика"""
        vaccination = self.get_object()
        cat = vaccination.cat
        cat_vaccinations = Vaccination.objects.filter(cat=cat).order_by('-vaccination_date')
        serializer = self.get_serializer(cat_vaccinations, many=True)
        return Response({
            'cat': cat.name,
            'count': cat_vaccinations.count(),
            'vaccinations': serializer.data
        })