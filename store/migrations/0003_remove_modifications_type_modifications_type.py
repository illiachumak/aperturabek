# Generated by Django 4.2 on 2024-01-06 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_modifications_type_modifications_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modifications',
            name='type',
        ),
        migrations.AddField(
            model_name='modifications',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.modificationtype'),
        ),
    ]
