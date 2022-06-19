from posixpath import basename
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from codex.views.data.items import MagicItemViewSet
from codex.views.data.dungeonmaster import DMLogViewSet
from codex.views.data.character import CharacterViewSet
from codex.views.data.character_images import CharacterImageView

from codex.views.events.dm_rewards import DMRewardViewSet
from codex.views.events.dm_games import DMGamesViewSet
from codex.views.events.dm_events import DMEventView


router = DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'magicitem', MagicItemViewSet, basename='magicitem')
router.register(r'dm_log', DMLogViewSet, basename='dm_log')
router.register(r'dm_reward', DMRewardViewSet, basename='dm_reward')
router.register(r'dm_game', DMGamesViewSet, basename='dm_game')

urlpatterns = [
    path('dm_events/<uuid:dm_uuid>', DMEventView.as_view(), name='dm_events'),
    re_path('^dm_events/*', DMEventView.as_view(), name='dm_events'),
    re_path('^character/(?P<id>[0-9]+)/(?P<image_type>(artwork|token))/?', CharacterImageView.as_view(), name='character_artwork')
]

urlpatterns += router.urls
