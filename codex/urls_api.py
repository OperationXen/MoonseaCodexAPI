from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from codex.views.data.character import CharacterViewSet
from codex.views.data.items import MagicItemViewSet


router = DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'magicitem', MagicItemViewSet, basename='magicitem')

urlpatterns = router.urls
