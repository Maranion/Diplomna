# Generated by Django 3.1.3 on 2022-04-27 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_investment_simulator', '0002_auto_20220427_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='name',
            field=models.CharField(default='null', max_length=20),
        ),
    ]
