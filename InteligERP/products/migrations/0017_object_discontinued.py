# Generated by Django 4.2.3 on 2023-11-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_price_object'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='discontinued',
            field=models.BooleanField(default=False),
        ),
    ]