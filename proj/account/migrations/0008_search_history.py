# Generated by Django 2.0.13 on 2019-08-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20190713_2006'),
    ]

    operations = [
        migrations.CreateModel(
            name='search_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mincost', models.CharField(max_length=300, null=True)),
                ('maxcost', models.CharField(max_length=300, null=True)),
                ('keywd', models.CharField(max_length=300, null=True)),
                ('services', models.CharField(max_length=300, null=True)),
            ],
        ),
    ]
