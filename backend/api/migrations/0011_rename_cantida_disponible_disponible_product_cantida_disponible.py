# Generated by Django 5.1.1 on 2024-12-04 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_rename_cantidad_movimientostock_cantida_disponible_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='cantida_disponible_disponible',
            new_name='cantida_disponible',
        ),
    ]