# Generated by Django 3.2.18 on 2023-05-08 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('goodsName', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('kind', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inventory', models.IntegerField()),
                ('mainImg', models.ImageField(upload_to='static/img')),
                ('img1', models.ImageField(upload_to='static/img')),
                ('img2', models.ImageField(upload_to='static/img')),
                ('img3', models.ImageField(upload_to='static/img')),
                ('intro', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('userName', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=16)),
                ('authority', models.CharField(max_length=8)),
                ('email1', models.EmailField(max_length=32)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('loginTime', models.CharField(blank=True, max_length=32, null=True)),
                ('logoutTime', models.CharField(blank=True, max_length=32, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBrowsingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('goodsName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goods')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.members')),
            ],
        ),
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation', models.CharField(max_length=16)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.members')),
            ],
        ),
        migrations.AddField(
            model_name='goods',
            name='userName',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.members'),
        ),
        migrations.CreateModel(
            name='BuyLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('totalPrice', models.IntegerField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('goodsName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goods')),
                ('userName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.members')),
            ],
        ),
    ]
