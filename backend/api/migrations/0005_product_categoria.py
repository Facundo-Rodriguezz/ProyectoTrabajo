# Generated by Django 5.1.1 on 2024-11-10 23:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_product_categoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categoria',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='api.categoria'),
        ),
    ]
