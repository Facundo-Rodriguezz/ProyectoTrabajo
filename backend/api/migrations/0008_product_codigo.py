# Generated by Django 5.1.1 on 2024-11-26 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='codigo',
            field=models.CharField(default='abc', max_length=100),
            preserve_default=False,
        ),
    ]
