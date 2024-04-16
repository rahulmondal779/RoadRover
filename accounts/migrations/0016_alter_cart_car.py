# Generated by Django 5.0 on 2024-04-16 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_cart_car'),
        ('cars', '0009_alter_coupon_coupon_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.car'),
        ),
    ]
