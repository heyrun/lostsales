# Generated by Django 3.1 on 2020-08-20 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200820_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='attributes',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='size',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
