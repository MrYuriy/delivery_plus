# Generated by Django 5.0.1 on 2024-01-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delivery",
            name="identifier",
            field=models.BigIntegerField(default=20240119280, unique=True),
        ),
        migrations.RemoveField(
            model_name="delivery",
            name="images_url",
        ),
        migrations.AddField(
            model_name="delivery",
            name="images_url",
            field=models.ManyToManyField(blank=True, to="delivery.imagemodel"),
        ),
    ]
