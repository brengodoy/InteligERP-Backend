# Generated by Django 4.2.3 on 2023-11-03 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stakeholders', '0004_alter_client_cuil_alter_client_address_and_more'),
        ('products', '0005_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='object',
            name='supplier',
        ),
        migrations.AddField(
            model_name='price',
            name='supplier',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stakeholders.supplier', verbose_name='the supplier of the product'),
        ),
    ]
