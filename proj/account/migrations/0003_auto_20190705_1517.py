# Generated by Django 2.0.13 on 2019-07-05 15:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190705_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_order',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 5, 15, 17, 14, 366595, tzinfo=utc)),
        ),
    ]
