# Generated by Django 2.0.13 on 2019-09-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_deletedcustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='deletedcustomer',
            name='msg',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
    ]
