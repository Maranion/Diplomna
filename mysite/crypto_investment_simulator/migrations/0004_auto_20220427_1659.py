# Generated by Django 3.1.3 on 2022-04-27 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_investment_simulator', '0003_wallet_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='data',
        ),
        migrations.CreateModel(
            name='key_val',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=20)),
                ('value', models.DecimalField(db_index=True, decimal_places=100, max_digits=100)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crypto_investment_simulator.wallet')),
            ],
        ),
    ]