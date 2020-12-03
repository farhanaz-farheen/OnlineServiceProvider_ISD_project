# Generated by Django 2.0.13 on 2019-07-06 10:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20190705_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordered_service',
            name='deliveryAddress',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='ordered_service',
            name='desc',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ordered_service',
            name='expTime',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 6, 10, 5, 17, 697585, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='order',
            name='time_order',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 6, 10, 5, 17, 695070, tzinfo=utc)),
        ),
    ]