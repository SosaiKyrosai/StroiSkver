# Generated by Django 4.2.1 on 2023-06-28 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]