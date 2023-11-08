# Generated by Django 4.2.3 on 2023-11-03 18:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stakeholders', '0004_alter_client_cuil_alter_client_address_and_more'),
        ('products', '0016_alter_price_object'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('client', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stakeholders.client', verbose_name='client related to the sale')),
            ],
        ),
        migrations.CreateModel(
            name='sale_object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=1, max_digits=20)),
                ('object', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.object', verbose_name='object')),
                ('sale', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='transactions.sale', verbose_name='sale')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('total_cost', models.DecimalField(decimal_places=3, max_digits=20, null=True)),
                ('supplier', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='stakeholders.supplier', verbose_name='supplier related to the purchase')),
            ],
        ),
        migrations.AddConstraint(
            model_name='sale_object',
            constraint=models.UniqueConstraint(fields=('sale', 'object'), name='unique_sale_object'),
        ),
        migrations.AddConstraint(
            model_name='sale',
            constraint=models.UniqueConstraint(fields=('date', 'client'), name='unique_date_client'),
        ),
    ]