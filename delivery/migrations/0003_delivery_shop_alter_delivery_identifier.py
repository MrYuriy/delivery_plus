# Generated by Django 5.0.1 on 2024-01-22 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_alter_delivery_identifier_remove_delivery_images_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.shop'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='identifier',
            field=models.BigIntegerField(default=20240122694, unique=True),
        ),
    ]