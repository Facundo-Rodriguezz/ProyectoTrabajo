# Generated by Django 5.1.1 on 2024-12-17 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_remove_product_eliminado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientostock',
            name='cantidad_disponible',
            field=models.IntegerField(),
        ),
    ]
