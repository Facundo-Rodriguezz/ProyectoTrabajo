# Generated by Django 5.1.1 on 2024-10-09 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_categoria_rename_name_product_nombre_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='descripcion',
        ),
    ]