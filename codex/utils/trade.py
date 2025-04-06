from codex.models.items import MagicItem


def remove_adverts_for_item(item: MagicItem):
    adverts = item.adverts.all()
    adverts.delete()
