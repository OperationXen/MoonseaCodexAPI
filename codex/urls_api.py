from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from codex.tests.views.data.test_views_data_dungeonmaster import DungeonMasterLogCRUDViews

from codex.views.data.character import CharacterViewSet
from codex.views.data.items import MagicItemViewSet
from codex.views.data.dungeonmaster import DMLogViewSet


router = DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'magicitem', MagicItemViewSet, basename='magicitem')
router.register(r'dm_log', DMLogViewSet, basename='dm_log')

urlpatterns = router.urls
