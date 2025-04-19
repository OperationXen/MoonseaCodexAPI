from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from codex.views.data.items.magicitems import MagicItemViewSet
from codex.views.data.items.reference_items import ReferenceMagicItemViewSet
from codex.views.data.items.consumables import ConsumableItemViewSet
from codex.views.data.items.reference_consumables import ReferenceConsumableViewSet
from codex.views.data.dungeonmaster import DMLogViewSet
from codex.views.data.character import CharacterViewSet
from codex.views.data.character_images import CharacterImageView
from codex.views.data.items.sources import ItemSourceView
from codex.views.imports.character import CharacterImportView

from codex.views.events.magicitem_events import MagicItemEventView
from codex.views.events.character_events import CharacterEventView
from codex.views.events.games import CharacterGamesViewSet
from codex.views.events.player_games import PlayerGamesViewSet
from codex.views.events.events_dt_spellbook_update import EventDowntimeSpellbookUpdateView
from codex.views.events.events_dt_freeform import EventDowntimeFreeFormView
from codex.views.events.dm_rewards import DMRewardViewSet
from codex.views.events.dm_games import DMGamesViewSet
from codex.views.events.dm_events import DMEventView
from codex.views.events.games_search import SearchGamesView

from codex.views.trade.adverts import TradeAdvertView
from codex.views.trade.offers import TradeOfferView
from codex.views.trade.action import TradeActionView


router = DefaultRouter(trailing_slash=False)
router.register(r"character", CharacterViewSet, basename="character")
router.register(r"magicitem", MagicItemViewSet, basename="magicitem")
router.register(r"reference_item", ReferenceMagicItemViewSet, basename="reference_item")
router.register(r"consumable", ConsumableItemViewSet, basename="consumable")
router.register(r"reference_consumable", ReferenceConsumableViewSet, basename="reference_consumable")
router.register(r"game", CharacterGamesViewSet, basename="game")
router.register(r"games", PlayerGamesViewSet, basename="games")
router.register(r"dm_log", DMLogViewSet, basename="dm_log")
router.register(r"dm_reward", DMRewardViewSet, basename="dm_reward")
router.register(r"dm_game", DMGamesViewSet, basename="dm_game")
router.register(r"spellbook", EventDowntimeSpellbookUpdateView, basename="spellbook_update")
router.register(r"freeform", EventDowntimeFreeFormView, basename="freeform")


urlpatterns = [
    path("dm_events/<uuid:dm_uuid>", DMEventView.as_view(), name="dm_events"),
    path("character_events/<uuid:character_uuid>", CharacterEventView.as_view(), name="character_events"),
    # search views
    re_path(r"^game/search/?", SearchGamesView.as_view(), name="game_search"),
    # Event views
    re_path(r"^dm_events/*", DMEventView.as_view(), name="dm_events"),
    re_path(
        r"^magicitem/events/(?P<magicitem_uuid>[0-9a-f\-]{36})/?",
        MagicItemEventView.as_view(),
        name="magicitem_events",
    ),
    # Item source search
    re_path(r"^magicitem/source/?", ItemSourceView.as_view(), name="item_source"),
    # Trade views ('advert' and 'offer' avoided to bypass adblockers)
    re_path(
        r"^magicitem/faeproposal/(?P<action>(accept|reject))/(?P<uuid>[0-9a-f\-]{36})/?",
        TradeActionView.as_view(),
        name="trade_action",
    ),
    re_path(r"^magicitem/faeproposal/?(?P<uuid>[0-9a-f\-]{36})?/?", TradeOfferView.as_view(), name="offer"),
    re_path(r"^magicitem/faesuggestion/?(?P<uuid>[0-9a-f\-]{36})?/?", TradeAdvertView.as_view(), name="advert"),
    # Character and item views
    re_path(
        r"^character/(?P<uuid>[0-9a-f\-]{36})/(?P<image_type>(artwork|token))/?",
        CharacterImageView.as_view(),
        name="character_artwork",
    ),
    re_path(r"^character_import/?", CharacterImportView.as_view(), name="character_import"),
]

urlpatterns += router.urls
