# Generated by Django 5.1.1 on 2024-10-19 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_description_product_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='categoria',
        ),
    ]