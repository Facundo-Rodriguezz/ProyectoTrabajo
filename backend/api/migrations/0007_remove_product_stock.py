# Generated by Django 5.1.1 on 2024-11-14 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_product_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]