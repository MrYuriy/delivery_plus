# Generated by Django 5.0.1 on 2024-02-17 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0013_alter_location_work_zone"),
    ]

    operations = [
        migrations.AddField(
            model_name="delivery",
            name="complite_status",
            field=models.BooleanField(default=False),
        ),
    ]
