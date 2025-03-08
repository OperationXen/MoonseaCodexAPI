# Generated by Django 5.1.6 on 2025-03-05 21:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codex", "0020_alter_catchingup_datetime_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
