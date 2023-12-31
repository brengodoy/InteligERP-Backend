# Generated by Django 4.2.3 on 2023-11-01 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_alter_warehouse_id_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_section', models.IntegerField(null=True)),
                ('height', models.IntegerField()),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('max_weight', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('id_warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.warehouse')),
            ],
        ),
    ]
