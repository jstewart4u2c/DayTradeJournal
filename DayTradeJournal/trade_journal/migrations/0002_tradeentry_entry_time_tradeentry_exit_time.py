# Generated by Django 5.1.4 on 2025-06-22 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_journal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradeentry',
            name='entry_time',
            field=models.TimeField(default=datetime.time(8, 30)),
        ),
        migrations.AddField(
            model_name='tradeentry',
            name='exit_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
