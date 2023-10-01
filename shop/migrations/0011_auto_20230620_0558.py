# Generated by Django 3.2.18 on 2023-06-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20230517_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buylog',
            name='logjson',
        ),
        migrations.AddField(
            model_name='buylog',
            name='goodsName',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buylog',
            name='num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buylog',
            name='orderNumber',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='buylog',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]
