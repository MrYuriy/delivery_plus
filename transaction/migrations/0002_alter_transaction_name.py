# Generated by Django 5.0.1 on 2024-02-27 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transaction", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="name",
            field=models.CharField(
                choices=[
                    ("Recive", "Recive"),
                    ("Relocate", "Relocate"),
                    ("Optimization", "Optimization"),
                    ("Shiped", "Shiped"),
                    ("Utilization", "Utilization"),
                ]
            ),
        ),
    ]
