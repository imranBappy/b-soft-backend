# Generated by Django 5.1.3 on 2025-01-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='images',
        ),
        migrations.AddField(
            model_name='product',
            name='photo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
