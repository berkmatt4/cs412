# Generated by Django 5.1.5 on 2025-02-18 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article", name="image_url", field=models.URLField(blank=True),
        ),
    ]
