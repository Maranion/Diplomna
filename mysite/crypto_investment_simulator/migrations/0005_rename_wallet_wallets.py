# Generated by Django 4.0 on 2022-05-04 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_investment_simulator', '0004_rename_name_wallet_user_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Wallet',
            new_name='Wallets',
        ),
    ]
