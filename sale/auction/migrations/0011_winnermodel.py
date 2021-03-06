# Generated by Django 3.1.4 on 2021-12-03 02:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0010_auto_20211201_1810'),
    ]

    operations = [
        migrations.CreateModel(
            name='WinnerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auction.listingmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
