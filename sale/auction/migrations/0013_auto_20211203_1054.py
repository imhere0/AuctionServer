# Generated by Django 3.1.4 on 2021-12-03 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0012_auto_20211203_0825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='winnermodel',
            old_name='listing_id',
            new_name='listingid',
        ),
    ]
