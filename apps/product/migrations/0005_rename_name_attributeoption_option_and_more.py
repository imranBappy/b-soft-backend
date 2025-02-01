# Generated by Django 5.1.3 on 2025-01-27 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_coupon_remove_product_tax_attribute_attributeoption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attributeoption',
            old_name='name',
            new_name='option',
        ),
        migrations.AddField(
            model_name='attributeoption',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
