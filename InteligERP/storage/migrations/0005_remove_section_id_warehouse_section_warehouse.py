# Generated by Django 4.2.3 on 2023-11-01 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='id_warehouse',
        ),
        migrations.AddField(
            model_name='section',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='storage.warehouse', verbose_name='the related warehouse'),
        ),
    ]
