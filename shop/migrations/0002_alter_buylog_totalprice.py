# Generated by Django 3.2.18 on 2023-05-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buylog',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
