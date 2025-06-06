# Generated by Django 5.1.6 on 2025-04-27 18:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codex", "0025_referenceconsumable_referencemagicitem"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="consumable",
            name="content_type",
            field=models.ForeignKey(
                help_text="Type of event that resulted in this object coming to you",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
                verbose_name="Origin Type",
            ),
        ),
        migrations.AddField(
            model_name="consumable",
            name="object_id",
            field=models.PositiveIntegerField(
                help_text="ID of the specific source event",
                null=True,
                verbose_name="Event ID",
            ),
        ),
    ]
