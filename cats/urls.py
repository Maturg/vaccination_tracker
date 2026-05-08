from rest_framework.routers import DefaultRouter
from .views import CatViewSet, AchievementViewSet

router = DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = router.urls