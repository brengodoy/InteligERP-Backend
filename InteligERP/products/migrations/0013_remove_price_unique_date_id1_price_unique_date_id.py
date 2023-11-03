# Generated by Django 4.2.3 on 2023-11-03 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_remove_price_unique_date_id_price_unique_date_id1'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='price',
            name='unique_date_id1',
        ),
        migrations.AddConstraint(
            model_name='price',
            constraint=models.UniqueConstraint(fields=('object', 'date'), name='unique_date_id'),
        ),
    ]
