# Generated by Django 5.2.4 on 2025-07-19 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GENERAL_APPS', '0005_checklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='status',
            field=models.CharField(default='1', max_length=255),
        ),
    ]
