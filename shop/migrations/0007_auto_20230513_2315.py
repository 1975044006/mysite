# Generated by Django 3.2.18 on 2023-05-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20230513_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='img1',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='mainImg',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
    ]
