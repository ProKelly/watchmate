# Generated by Django 4.2.7 on 2024-01-20 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0003_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='update',
            new_name='updated',
        ),
    ]
