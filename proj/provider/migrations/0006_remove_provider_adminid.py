# Generated by Django 2.0.13 on 2019-06-29 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0005_auto_20190628_1322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='adminid',
        ),
    ]
