# Generated by Django 5.1.5 on 2025-04-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='year',
            field=models.IntegerField(),
        ),
    ]
