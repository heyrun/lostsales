# Generated by Django 3.1.2 on 2020-10-06 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200910_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='subsidiary',
            field=models.CharField(choices=[('100', 'HealthPlus'), ('200', 'CasaBella')], max_length=20),
        ),
    ]
