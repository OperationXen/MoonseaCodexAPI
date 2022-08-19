# Generated by Django 4.0.4 on 2022-08-19 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codex', '0005_trade_datetime_trade_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='associated',
            field=models.ForeignKey(blank=True, help_text='The other half of the trade', null=True, on_delete=django.db.models.deletion.SET_NULL, to='codex.trade'),
        ),
    ]
