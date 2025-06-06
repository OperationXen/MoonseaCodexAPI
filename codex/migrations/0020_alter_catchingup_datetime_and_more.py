# Generated by Django 5.1.6 on 2025-02-23 17:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codex", "0019_remove_magicitem_item_tradable_idx_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="catchingup",
            name="datetime",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
        migrations.AlterField(
            model_name="mundanetrade",
            name="datetime",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
        migrations.AlterField(
            model_name="spellbookupdate",
            name="datetime",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]
