# Generated by Django 4.0.8 on 2025-06-22 03:15

import datetime
from django.db import migrations, models
# from django.utils.timezone import utc
from datetime import datetime, timezone

class Migration(migrations.Migration):
    utc = datetime.now(timezone.utc)

    dependencies = [
        ('DOCMA', '0008_alter_docma_firebase_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docma_firebase',
            name='end_date',
            field=models.DateField(verbose_name=datetime(2025, 6, 22, 3, 15, 44, 868096, tzinfo=timezone.utc)),
        ),
        migrations.AlterField(
            model_name='docma_firebase',
            name='start_date',
            field=models.DateField(verbose_name=datetime(2025, 6, 22, 3, 15, 44, 868096, tzinfo=timezone.utc)),
        ),
    ]
