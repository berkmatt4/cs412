# Generated by Django 5.1.5 on 2025-04-17 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_alter_vehicle_year"),
    ]

    operations = [
        migrations.AddField(
            model_name="vehicle",
            name="image",
            field=models.ImageField(blank=True, upload_to=""),
        ),
    ]
