# Generated by Django 2.0.13 on 2019-09-08 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_remove_customer_regdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search_history',
            name='keywd',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='maxcost',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='mincost',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='search_history',
            name='services',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
