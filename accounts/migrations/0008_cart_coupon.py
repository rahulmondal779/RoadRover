# Generated by Django 5.0 on 2024-04-04 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_wishlistitems_user'),
        ('cars', '0009_alter_coupon_coupon_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cars.coupon'),
        ),
    ]
