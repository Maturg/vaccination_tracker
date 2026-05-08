from rest_framework.routers import DefaultRouter
from .views import CatViewSet, VaccineViewSet, VaccinationViewSet

router = DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'vaccines', VaccineViewSet)
router.register(r'vaccinations', VaccinationViewSet)

urlpatterns = router.urls