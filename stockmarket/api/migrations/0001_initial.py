# Generated by Django 5.0.1 on 2024-01-25 09:49

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('open_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('close_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('high', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('low', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('volume', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(choices=[('buy', 'Buy'), ('sell', 'Sell')], max_length=4)),
                ('transaction_volume', models.PositiveIntegerField()),
                ('transaction_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.stockdata')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
    ]
