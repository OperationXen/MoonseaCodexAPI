from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from codex.views.data.magicitems import MagicItemViewSet
from codex.views.data.dungeonmaster import DMLogViewSet
from codex.views.data.character import CharacterViewSet
from codex.views.data.character_images import CharacterImageView
from codex.views.data.discord import DiscordBotQueryView

from codex.views.events.magicitem_events import MagicItemEventView
from codex.views.events.character_events import CharacterEventView
from codex.views.events.character_games import CharacterGamesViewSet
from codex.views.events.dm_rewards import DMRewardViewSet
from codex.views.events.dm_games import DMGamesViewSet
from codex.views.events.dm_events import DMEventView

from codex.views.trade.status import TradeStatusView
from codex.views.trade.adverts import TradeAdvertView


router = DefaultRouter()
router.register(r'character', CharacterViewSet, basename='character')
router.register(r'magicitem', MagicItemViewSet, basename='magicitem')
router.register(r'game', CharacterGamesViewSet, basename='game')
router.register(r'dm_log', DMLogViewSet, basename='dm_log')
router.register(r'dm_reward', DMRewardViewSet, basename='dm_reward')
router.register(r'dm_game', DMGamesViewSet, basename='dm_game')

urlpatterns = [
    path('dm_events/<uuid:dm_uuid>', DMEventView.as_view(), name='dm_events'),
    path('character_events/<uuid:character_uuid>', CharacterEventView.as_view(), name='character_events'),
    re_path('^dm_events/*', DMEventView.as_view(), name='dm_events'),
    re_path('^magicitem/events/(?P<magicitem_uuid>[0-9a-f\-]{36})/?', MagicItemEventView.as_view(), name='magicitem_events'),
    re_path('^magicitem/trade/(?P<magicitem_uuid>[0-9a-f\-]{36})/?', TradeStatusView.as_view(), name='magicitem_trade_status'),
    re_path('^magicitem/advert/?(?P<uuid>[0-9a-f\-]{36})?/?', TradeAdvertView.as_view(), name='advert'),
    re_path('^character/(?P<uuid>[0-9a-f\-]{36})/(?P<image_type>(artwork|token))/?', CharacterImageView.as_view(), name='character_artwork'),
    re_path('^discord_lookup/(?P<query_type>(character|items))/', DiscordBotQueryView.as_view(), name='discord_lookup')
]

urlpatterns += router.urls
