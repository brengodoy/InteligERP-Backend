# Generated by Django 4.2.3 on 2023-11-02 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_object_height_alter_object_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='object',
            name='product_id',
            field=models.IntegerField(null=True, unique=True),
        ),
    ]