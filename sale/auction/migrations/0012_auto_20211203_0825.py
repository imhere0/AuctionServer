# Generated by Django 3.1.4 on 2021-12-03 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0011_winnermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidmodel',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
