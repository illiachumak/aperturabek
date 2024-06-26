# Generated by Django 4.2 on 2024-01-15 09:32

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_order_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='color',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='modifications',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
    ]
