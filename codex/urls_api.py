from rest_framework.routers import DefaultRouter

from codex.views.data.character import CharacterViewSet


router = DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')

urlpatterns = router.urls
