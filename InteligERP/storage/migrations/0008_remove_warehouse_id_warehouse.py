# Generated by Django 4.2.3 on 2023-12-15 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0007_section_available_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='warehouse',
            name='id_warehouse',
        ),
    ]