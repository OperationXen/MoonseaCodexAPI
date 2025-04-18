# Generated by Django 5.1.6 on 2025-04-18 13:16

import django.db.models.deletion
import django.db.models.functions.text
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codex", "0024_remove_mundanetrade_character_delete_catchingup_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReferenceConsumable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("name", models.CharField(help_text="Item Name", max_length=256)),
                (
                    "type",
                    models.TextField(
                        choices=[
                            ("scroll", "Spell scroll"),
                            ("potion", "Potion"),
                            ("ammo", "Ammunition"),
                            ("gear", "Adventuring Gear"),
                            ("other", "Other item"),
                        ],
                        default="scroll",
                        help_text="Item type",
                    ),
                ),
                (
                    "charges",
                    models.IntegerField(
                        blank=True, help_text="Number of charges", null=True
                    ),
                ),
                (
                    "rarity",
                    models.CharField(
                        choices=[
                            ("common", "Common"),
                            ("uncommon", "Uncommon"),
                            ("rare", "Rare"),
                            ("veryrare", "Very Rare"),
                            ("legendary", "Legendary"),
                        ],
                        default="uncommon",
                        help_text="Item rarity",
                        max_length=16,
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="consumables",
                        to="codex.game",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReferenceMagicItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("name", models.CharField(help_text="Base item name", max_length=256)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "flavour",
                    models.TextField(blank=True, help_text="Flavour text", null=True),
                ),
                (
                    "rp_name",
                    models.TextField(blank=True, help_text="Roleplay name", null=True),
                ),
                (
                    "minor_properties",
                    models.TextField(
                        blank=True,
                        help_text="Minor properties - guardian, etc",
                        null=True,
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        blank=True, help_text="Link to item details", null=True
                    ),
                ),
                (
                    "rarity",
                    models.CharField(
                        choices=[
                            ("common", "Common"),
                            ("uncommon", "Uncommon"),
                            ("rare", "Rare"),
                            ("veryrare", "Very Rare"),
                            ("legendary", "Legendary"),
                        ],
                        default="uncommon",
                        help_text="Item rarity",
                        max_length=16,
                    ),
                ),
                (
                    "attunement",
                    models.BooleanField(
                        default=False, help_text="Item requires attunement to be used"
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="magicitems",
                        to="codex.game",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["uuid"], name="refitem_uuid_idx"),
                    models.Index(fields=["name"], name="refitem_name_idx"),
                    models.Index(fields=["rp_name"], name="refitem_rp_name_idx"),
                    models.Index(
                        django.db.models.functions.text.Upper("name"),
                        name="refitem_name_upper_idx",
                    ),
                    models.Index(
                        django.db.models.functions.text.Upper("rp_name"),
                        name="refitem_rp_name_upper_idx",
                    ),
                ],
            },
        ),
    ]
