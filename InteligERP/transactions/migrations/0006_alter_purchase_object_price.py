# Generated by Django 4.2.3 on 2023-11-05 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_purchase_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase_object',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
